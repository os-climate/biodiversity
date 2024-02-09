from sostrades_core.study_manager.study_manager import StudyManager


class Study(StudyManager):

    def __init__(self, execution_engine=None):
        super().__init__(__file__, execution_engine=execution_engine)

    def setup_usecase(self):

        dict_values = {
            f'{self.study_name}.Seamed_model.Temparture': 15.3,
            f'{self.study_name}.Seamed_model.Urbansiation':1.7*10**5,
            f'{self.study_name}.Seamed_model.Fishing_med': 1764*10**3,
            f'{self.study_name}.Seamed_model.PlasticConsumption':53000000,
            f'{self.study_name}.Seamed_model.PlasticNorms':0.5,
            f'{self.study_name}.Seamed_model.ChemicalWaste':3145.6,
            f'{self.study_name}.Seamed_model.Tourism':183,
            f'{self.study_name}.Seamed_model.Renewal':300000, 
            }
        return dict_values


if '__main__' == __name__:
    uc_cls = Study()
    uc_cls.load_data()
    uc_cls.run(for_test=True)
    
