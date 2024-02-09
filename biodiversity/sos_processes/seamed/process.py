from sostrades_core.sos_processes.base_process_builder import BaseProcessBuilder


class ProcessBuilder(BaseProcessBuilder):

    # ontology information
    _ontology_data = {
        'label': 'Seamed_Process',
        'description': '',
        'category': 'Research',
        'version': '0.1',
    }

    def get_builders(self):
        mod_path = 'biodiversity.biodiversity.sos_wrapping.seamed'
        builder = self.ee.factory.get_builder_from_module(
            'seamed', mod_path)
        return builder