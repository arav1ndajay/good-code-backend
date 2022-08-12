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

        # print(self.df['date'] == datetime.datetime.strptime(
        #     date, "%Y").date())

        return self.df.loc[(self.df['date'] == datetime.datetime.strptime(
            date, "%d_%m_%Y").date()) & (self.df['camera_id'] == camera_id)]

    def get_info(self, camera_id: str, date: str):

        survey_entries = self.get_entry(camera_id=camera_id, date=date)
        survey_dict = survey_entries.to_dict()

        x, y = survey_dict['SHAPE'][0].x, survey_dict['SHAPE'][0].y
        project_name = survey_dict['project_name'][0]
        camera_setup_date = survey_dict['date_and_time_of_camera_setup_o'][0]
        procedure = survey_dict['_procedure'][0]
        camera_attached_to = survey_dict['camera_attached_to'][0]
        camera_height = survey_dict['camera_height'][0]
        area_deployed = survey_dict['name_of_area_deployed'][0]
        camera_make = survey_dict['camera_make'][0]
        camera_settings = survey_dict['camera_settings'][0]
        camera_feature = survey_dict['what_feature_is_the_camera_targ'][0]
        camera_trap_test = survey_dict['camera_trap_test'][0]
        camera_working = survey_dict['camera_working_when_you_left_or'][0]

        info_dict = {
            'X': x,
            'Y': y,
            'Camera setup date': camera_setup_date,
            'Project Name': project_name,
            'Procedure': procedure,
            'Camera attached to': camera_attached_to,
            'Camera height': camera_height,
            'Area deployed': area_deployed,
            'Camera make': camera_make,
            'Camera settings': camera_settings,
            'Camera feature': camera_feature,
            'Camera trap test': camera_trap_test,
            'Camera working when left': camera_working
        }

        return info_dict


survey = CameraTrapSurvey(url="https://learngis2.maps.arcgis.com/",
                          username="0627130_LearnArcGIS",
                          password="arcgispass@123",
                          survey_id="bcafa6fa2e584123a4f2715474cf6327")
