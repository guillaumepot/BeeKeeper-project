#airflow/code/dags/utils/segmentation_functions.py



# LIB
import datetime as datetime
import numpy as np
import pandas as pd
import pickle
import piecewise_regression

from utils.logger import basic_logger



def segment_weight(df, weight_reference = "poids_max", date = "date", scale_column = "bal", scale = None, year0 = 2022, month0 = 1, day0 = 1, n_breakpoints = 7):
    """
    Description :
    This function take automatic scale datas, perform piecewise-regression and return a dataframe containing the following columns :
    Segment : an index of segment (starting from 1)
    Start : the number of days since day0 at the segment's start.
    End : the number of days since day0 at the segment's end.
    Slope : segment's linear regression slope.
    Weight Start : weight at the segment's beginning.
    Weight End : weight at the segment's end.
    Weight Diff : the weight difference beetwin end and start.
    ---
    Arguments : 
    df : a pandas dataframe containing the scale label, the date, and the measured weight
    date : name of the date's column
    weight : name of the weight's column
    scale : name of the scale label's column
    year0, month0, day0 : the origin date used to convert date as numeric (required for regression purpose)
    n_breakpoints : number of breakpoints to use for piecewiese regression.
    ---
    Dependencies : 
    pandas, datetime, numpy, piecewise_regression
    """

    if scale == None: return "A scale must be provide"
    
    else :
        
        df_scale = df.loc[df[scale_column] == scale,]

        x = pd.to_datetime(df_scale[date]).map(lambda x: (x - datetime.datetime(year0, month0, day0)).days)

        xx = x.to_list()
        yy = df_scale[weight_reference].to_list()
        
        pw_fit = piecewise_regression.Fit(xx, yy, n_breakpoints=n_breakpoints)

        results = pw_fit.get_results()

        # Extraction des breakpoints
        breakpoints = [
            (key, val["estimate"], val["confidence_interval"])
            for key, val in results["estimates"].items()
            if "breakpoint" in key
        ]

        # Extraction des pentes (alphas)
        coefficients = [
            (key, val["estimate"], val["confidence_interval"])
            for key, val in results["estimates"].items()
            if "alpha" in key
        ]

        # Convertir les breakpoints en liste triée
        breakpoint_positions = sorted([bp[1] for bp in breakpoints])

        # Ajouter les limites de l'intervalle initial et final
        breakpoint_positions = [min(xx)] + breakpoint_positions + [max(xx)]

        # Calcul des poids au début et à la fin de chaque segment
        segment_data = []
        for i, slope_info in enumerate(coefficients):
            slope = slope_info[1]  # Coefficient de la pente
            start = breakpoint_positions[i]
            end = breakpoint_positions[i + 1]

            # Calcul des poids au début et à la fin
            #weight_start = df_bal.loc[df_bal["date_numeric"] == np.round(start, 0)].poids_max.values   # pas si simple d'aller chercher les vraies valeurs, parfois le round(date, 0) ne mène à rien d'observé
            #weight_end = df_bal.loc[df_bal["date_numeric"] == np.round(end, 0)].poids_max.values       # mieux vaut passer par les predict
            weight_start = pw_fit.predict([start])
            weight_end = pw_fit.predict([end])

            segment_data.append({
                "Segment": i + 1,
                "Start": start,
                "End": end,
                "Slope": slope,
                "Weight Start": weight_start,
                "Weight End": weight_end,
                "Weight diff": weight_end - weight_start
            })

        # Création de la DataFrame des segments
        df_segments = pd.DataFrame(segment_data)
        df_segments["scale"] = scale
        
          # Liste des colonnes concernées

        for col in ["Weight Start", "Weight End", "Weight diff"]:
            df_segments[col] = df_segments[col].apply(lambda x: x[0] if isinstance(x, np.ndarray) else x)
        
        return df_segments, pw_fit



def segment_meteo(meteo_data, segment_data):
    """
    Description :
    This function returns meteo indicators based on certain period and is designed to be used after segment_weight function in an 'one by one scale' process.
    ---
    Arguments :
    meteo_data : a df containing meteo data to summarize by segment (must include scale's name).
    segment_data : df produced by 'segment_weight' function (item 'summary' in the returned list).
    ---
    Dependencies : pandas
    """

    scale = segment_data["scale"].values[0]
    meteo_scale = meteo_data.loc[meteo_data["bal"] == scale,]

    meteo_by_segment = {}
    
    for segment in segment_data["Segment"]:
        start = segment_data.loc[segment_data["Segment"] == segment, "Start"]
        end = segment_data.loc[segment_data["Segment"] == segment, "End"]
        meteo_segment_raw = meteo_scale.loc[(meteo_scale["date_numeric"] > start.values[0]) & (meteo_scale["date_numeric"] < end.values[0]),]

        # temperature_2m_min
        tmin = meteo_segment_raw['temperature_2m_min'].copy()
        tmin_dict = {
            "tmin_too_cold": sum((tmin <= 15)),                                      
            "tmin_opti"    : sum((tmin > 15) & (tmin <= 30)),  
            "tmin_hot"     : sum((tmin > 30) & (tmin <= 40)),  
            "tmin_too_hot" : sum((tmin > 40))                                        
        }

        # temperature_2m_max
        tmax = meteo_segment_raw['temperature_2m_max'].copy()
        tmax_dict = {
            "tmax_too_cold" : sum((tmax <= 15)),                                     # t_too_cold 
            "tmax_opti"     : sum((tmax > 15) & (tmax <= 30)), # t_opti
            "tmax_hot"      : sum((tmax > 30) & (tmax <= 40)), # t_hot
            "tmax_too_hot"  : sum((tmax > 40))                                      # t_too_hot
        }

        # Average wind
        wind_strength = {
            "days_weak_wind": sum((meteo_segment_raw["wind_speed_10m_max"] < 10.8)),
            "days_average_wind": sum((meteo_segment_raw["wind_speed_10m_max"] > 10.8) & (meteo_segment_raw["wind_speed_10m_max"] < 25.2)),
            "days_strong_wind": sum((meteo_segment_raw["wind_speed_10m_max"] > 25.2)) 
        }

        # wind direction
        wind_direction = {
            "N"  : sum((meteo_segment_raw["wind_direction_10m_dominant"] >= 337.5) | (meteo_segment_raw["wind_direction_10m_dominant"] <  22.5)),
            "NE" : sum((meteo_segment_raw["wind_direction_10m_dominant"] >=  22.5) & (meteo_segment_raw["wind_direction_10m_dominant"] <  67.5)),
            "E"  : sum((meteo_segment_raw["wind_direction_10m_dominant"] >=  67.5) & (meteo_segment_raw["wind_direction_10m_dominant"] < 112.5)),
            "SE" : sum((meteo_segment_raw["wind_direction_10m_dominant"] >= 112.5) & (meteo_segment_raw["wind_direction_10m_dominant"] < 157.5)),
            "S"  : sum((meteo_segment_raw["wind_direction_10m_dominant"] >= 157.5) & (meteo_segment_raw["wind_direction_10m_dominant"] < 202.5)),
            "SW" : sum((meteo_segment_raw["wind_direction_10m_dominant"] >= 202.5) & (meteo_segment_raw["wind_direction_10m_dominant"] < 247.5)),
            "W"  : sum((meteo_segment_raw["wind_direction_10m_dominant"] >= 247.5) & (meteo_segment_raw["wind_direction_10m_dominant"] < 292.5)),
            "NW" : sum((meteo_segment_raw["wind_direction_10m_dominant"] >= 292.5) & (meteo_segment_raw["wind_direction_10m_dominant"] < 337.5))
        }

        # Precipitation sum (by type)
        precipitation = {
            "precipitation":sum(meteo_segment_raw['precipitation_sum']),
            "rain":         sum(meteo_segment_raw['rain_sum']),
            "snowfall":     sum(meteo_segment_raw['snowfall_sum'])
        }

        # weather_code (simplified)
        weather_code = meteo_segment_raw['weather_code'].copy()
        weather_code.loc[(meteo_segment_raw['weather_code'] >=  0) & (meteo_segment_raw['weather_code'] <= 19)] = 1
        weather_code.loc[(meteo_segment_raw['weather_code'] >= 20) & (meteo_segment_raw['weather_code'] <= 29)] = 2
        weather_code.loc[(meteo_segment_raw['weather_code'] >= 30) & (meteo_segment_raw['weather_code'] <= 39)] = 3
        weather_code.loc[(meteo_segment_raw['weather_code'] >= 40) & (meteo_segment_raw['weather_code'] <= 49)] = 4
        weather_code.loc[(meteo_segment_raw['weather_code'] >= 50) & (meteo_segment_raw['weather_code'] <= 59)] = 5
        weather_code.loc[(meteo_segment_raw['weather_code'] >= 60) & (meteo_segment_raw['weather_code'] <= 69)] = 6
        weather_code.loc[(meteo_segment_raw['weather_code'] >= 70) & (meteo_segment_raw['weather_code'] <= 79)] = 7
        weather_code.loc[(meteo_segment_raw['weather_code'] >= 80) & (meteo_segment_raw['weather_code'] <= 99)] = 8

        weather_code = weather_code.value_counts().sort_index()
        weather_code.index = ["weather_code_" + str(key) for key in weather_code.index]
        weather_code = weather_code.to_dict()
    
        meteo_by_segment[segment] = pd.DataFrame([{"scale": scale} | tmin_dict | tmax_dict | wind_strength | wind_direction | precipitation | weather_code])
    
    meteo_segmented = pd.concat(meteo_by_segment.values(), keys=meteo_by_segment.keys()).reset_index(level=0)
    meteo_segmented.rename(columns={'level_0': 'Segment'}, inplace=True)
    meteo_segmented = meteo_segmented.reset_index(drop = True)
    meteo_segmented = meteo_segmented.fillna(0)
    
    return meteo_segmented



def df_segmentation_operation(**kwargs) -> pd.DataFrame:
    """
    Perform segmentation operation on a DataFrame and return the concatenated segmented DataFrame.

    This function retrieves a DataFrame from Airflow's XCom, segments the data by year and scale, 
    and applies weight and meteorological segmentation. The segmented data is then concatenated 
    and returned. Additionally, segmentation models are saved to disk.

    Args:
        **kwargs: Arbitrary keyword arguments.
            - task_instance: Airflow task instance to pull XCom data.
            - task_ids: Task IDs to pull XCom data.
            - segmentation_min_month: Minimum month for segmentation (e.g., "-01-01").
            - segmentation_max_month: Maximum month for segmentation (e.g., "-12-31").
            - model_savedir: Directory path to save segmentation models.

    Returns:
        pd.DataFrame: Concatenated segmented DataFrame.

    Raises:
        KeyError: If required keys are missing in kwargs.
        ValueError: If the DataFrame is empty or invalid.

    Notes:
        - The function assumes that the input DataFrame contains a 'date' column in string format 
          and a 'bal' column for balance.
        - The segmentation models are saved as pickle files in the specified directory.
    """
    # FUNCTION LOGIC
    task_instance = kwargs.get('task_instance')
    df = task_instance.xcom_pull(task_ids = kwargs["task_ids"])


    concatened_df_segments= pd.DataFrame()

    df["year"] = pd.to_datetime(df["date"]).dt.year
    for year in df["year"].unique():
        df_year = df.loc[
            (df["date"] > (str(year) + kwargs["segmentation_min_month"])) & 
            (df["date"] < (str(year) + kwargs["segmentation_max_month"]))
        ]

        segmented_bal = pd.DataFrame()
        segmentation_models: dict = {}

        if df_year.empty:
            basic_logger.warning(f"No data available for year {year}")
        else:
            df_year["date_numeric"] = pd.to_datetime(df_year["date"]).map(lambda x: (x - datetime.datetime(year, 1, 1)).days)

            for scale in df_year["bal"].unique():
                segmented_weight, segmentation_scale_model = segment_weight(df_year, scale = scale)
                segmented_meteo = segment_meteo(meteo_data=df_year, segment_data = segmented_weight)

                # Merge the two dataframes
                merged_segmented = segmented_weight.merge(segmented_meteo, on=["scale", "Segment"])
                segmented_bal = pd.concat([segmented_bal, merged_segmented])

                segmentation_models[f"segment_model_{year}-{scale}"] = segmentation_scale_model

        # Concat years
        concatened_df_segments = pd.concat([concatened_df_segments, segmented_bal])

        # Save the segmentation model
        for key, model in segmentation_models.items():
            with open(f"{kwargs['model_savedir']}/{key}.pkl", "wb") as f:
                pickle.dump(model, f)

    return concatened_df_segments