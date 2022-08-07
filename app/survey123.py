import arcgis
from arcgis.gis import GIS
import pandas as pd
import datetime


class CameraTrapSurvey:

    def __init__(self, url: str, username: str, password: str, survey_id: str):
        self.gis = GIS(url=url, username=username, password=password)
        self.survey_manager = arcgis.apps.survey123.SurveyManager(self.gis)
        self.survey_id = survey_id
        self.survey = self.survey_manager.get(self.survey_id)
        self.df = self.survey.download('DF')
        self.df['date'] = self.df['date_and_time_of_camera_setup_o'].dt.date

    def get_survey(self):
        return self.survey

    def get_survey_df(self):
        return self.df

    def get_entry(self, camera_id: str, date: str):

        return self.df.loc[(self.df['date'] == datetime.datetime.strptime(
            date, "%Y-%m-%d").date()) & (self.df['camera_id'] == camera_id)]


survey = CameraTrapSurvey(url="https://learngis2.maps.arcgis.com/",
                          username="0627130_LearnArcGIS",
                          password="arcgispass@123",
                          survey_id="bcafa6fa2e584123a4f2715474cf6327")
