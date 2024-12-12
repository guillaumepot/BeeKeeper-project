FROM debian:bookworm
LABEL maintainer "Alexandre Dangleant <alexandre.dangleant@itsap.asso.fr>"
# system libraries
RUN apt-get update
RUN apt-get update --fix-missing
RUN apt-get install -y --allow-unauthenticated dirmngr apt-transport-https ca-certificates software-properties-common gnupg2
RUN apt-get update 
RUN apt-get install -y --allow-unauthenticated \
    locales \
    r-base \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    libprotobuf-dev \
    protobuf-compiler \
    libudunits2-dev \
    libv8-dev \
    libjq-dev \
    libssl-dev
RUN apt-get update 
RUN apt-get install -y --allow-unauthenticated \ 
    libfontconfig1-dev
RUN apt-get update --fix-missing
RUN apt-get install -y --allow-unauthenticated \
    libcairo2-dev \
    r-cran-rmarkdown
#Set encoding
RUN sed -i '/fr_FR.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG fr_FR.UTF-8
ENV LC_ALL fr_FR.UTF-8
ENV TZ UTC
LABEL maintainer "Alexandre Dangleant <alexandre.dangleant@itsap.asso.fr>"
RUN R -e "install.packages('leaflet', repos='https://cloud.r-project.org/')"
RUN R -e "install.packages('leaflet.extras', repos='https://cloud.r-project.org/')"
RUN R -e "install.packages('shiny', repos='https://cloud.r-project.org/')"
RUN R -e "install.packages('htmlwidgets', repos='https://cloud.r-project.org/')"
RUN R -e "install.packages('htmltools', repos='https://cloud.r-project.org/')"
RUN R -e "install.packages('sf', repos='https://cloud.r-project.org/')"
RUN R -e "install.packages('DBI', repos='https://cloud.r-project.org/')"
RUN R -e "install.packages('DT', repos='https://cloud.r-project.org/')"
RUN R -e "install.packages('stringr', repos='https://cloud.r-project.org/')"
RUN R -e "install.packages('blastula', repos='https://cloud.r-project.org/')"
RUN R -e "install.packages('httr', repos='https://cloud.r-project.org/')"
RUN R -e "install.packages('openssl', repos='https://cloud.r-project.org/')"
RUN R -e "install.packages('shinyjs', repos='https://cloud.r-project.org/')"
RUN R -e "install.packages('password', repos='https://cloud.r-project.org/')"
RUN R -e "install.packages('RColorBrewer', repos='https://cloud.r-project.org/')"
RUN R -e "install.packages('shinycssloaders', repos='https://cloud.r-project.org/')"
RUN R -e "install.packages('shinyWidgets', repos='https://cloud.r-project.org/')"
RUN R -e "install.packages('rAmCharts', repos='https://cloud.r-project.org/')"
RUN R -e "install.packages('bslib', repos='https://cloud.r-project.org/')"
RUN R -e "install.packages('bsicons', repos='https://cloud.r-project.org/')"
RUN R -e "install.packages('RPostgres', repos='https://cloud.r-project.org/')"
RUN R -e "install.packages('plotly', repos='https://cloud.r-project.org/')"
# copy the apps to the image
COPY Rprofile.site /usr/lib/R/etc/
RUN mkdir /root/beegis/
# COPY beegis /root/beegis/  # Replaced as a volume in Docker-compose
EXPOSE 3838