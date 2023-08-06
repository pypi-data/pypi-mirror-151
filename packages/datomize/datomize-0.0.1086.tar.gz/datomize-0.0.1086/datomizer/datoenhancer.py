import io

from datomizer import DatoMapper
from datomizer.helpers import common_helper
from datomizer.helpers.train import enhance_ml_helper, train_helper
from datomizer.helpers.wrapper import schema_wrapper
from datomizer.utils.general import ID, MODELS, ERROR
from datomizer.utils.step_types import ML_TRAIN_AND_GENERATE
from datomizer.utils.enhance_ml import Metrics, Algorithms


class DatoEnhancer(object):
    dato_mapper: DatoMapper
    train_id = 0
    model_id = 0
    target_table = ""
    target_column = ""

    def __init__(self, dato_mapper: DatoMapper):
        """Create DatoTrainer object for training a generative model for the mapped input data.
        Args:
            dato_mapper: the DatoMapper object for the input data."""
        dato_mapper.next_step_validation()
        self.dato_mapper = dato_mapper

    @classmethod
    def restore(cls, dato_mapper: DatoMapper, train_id):
        dato_enhancer = cls(dato_mapper)
        dato_enhancer.train_id = train_id
        dato_enhancer.wait()
        return dato_enhancer

    def enhance(self, target_table: str = "", target_column: str = "",
                metric_list: [Metrics] = [], algorithm_list: [Algorithms] = [], wait=True) -> None:
        if self.train_id > 0:
            return

        metric_list = [metric.value for metric in metric_list]
        algorithm_list = [algorithm.value for algorithm in algorithm_list]

        self.target_table = self.dato_mapper.schema.table(target_table)[schema_wrapper.NAME]
        self.target_column = self.dato_mapper.schema.column(target_table, target_column)[schema_wrapper.NAME]

        self.train_id = enhance_ml_helper.enhance_ml_evaluate(self.dato_mapper,
                                                              target_table=self.target_table,
                                                              target_column=self.target_column,
                                                              metric_list=metric_list, algorithm_list=algorithm_list)
        if wait:
            self.wait()

    def wait(self) -> None:
        """Wait until the train method returns."""
        self.restore_validation()
        status = common_helper.wait_for_step_type(datomizer=self.dato_mapper.datomizer,
                                                  business_unit_id=self.dato_mapper.business_unit_id,
                                                  project_id=self.dato_mapper.project_id,
                                                  flow_id=self.dato_mapper.flow_id,
                                                  step_type=ML_TRAIN_AND_GENERATE,
                                                  train_id=self.train_id)
        if status == ERROR:
            raise Exception("Trainer Failed")
        train = train_helper.get_train_iteration(self.dato_mapper, self.train_id)
        self.model_id = train[MODELS][0][ID]

    def get_generated_data(self) -> None:
        self.restore_validation()
        print(common_helper.get_generated_zip(datomizer=self.dato_mapper.datomizer,
                                              business_unit_id=self.dato_mapper.business_unit_id,
                                              project_id=self.dato_mapper.project_id,
                                              flow_id=self.dato_mapper.flow_id,
                                              train_id=self.train_id))

    def get_generated_data_csv(self, table_name: str = None) -> io.StringIO:
        """Get the generated data in a csv format.
                Args:
                    table_name: the name of the generated data
                Returns:
                    StringIO object containing the generated data"""
        self.restore_validation()

        table_name = self.dato_mapper.schema.table(table_name)[schema_wrapper.NAME]

        return common_helper.get_generated_csv(datomizer=self.dato_mapper.datomizer,
                                               business_unit_id=self.dato_mapper.business_unit_id,
                                               project_id=self.dato_mapper.project_id,
                                               flow_id=self.dato_mapper.flow_id,
                                               train_id=self.train_id,
                                               table_name=table_name)

    def restore_validation(self):
        if not (self.train_id > 0):
            raise Exception("flow id required for this step")
