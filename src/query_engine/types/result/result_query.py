from src.infrastructure.types.omni_integer import OmniInteger


class QueryDataElement:
    def __init__(self, n: OmniInteger):
        self.value = n
        self.totient_element = None
        self.totient_log = None
        self.factor_set = None


class QueryDataCollection:
    def __init__(self, data_set: dict):
        self.data_set = data_set

        self.flat_totient_set = None
        self.extracted_totient_set = None

        self.ordered_int_set = []
        self.ordered_totient_set = []
        self.ordered_totient_time_set = []

    def flatten_totient(self):
        totient_set = dict()
        for data_int in self.data_set.keys():
            data_elem = self.data_set[data_int]
            tot_elem = data_elem.totient_element
            totient_ls = []
            while tot_elem is not None:
                tot_val = tot_elem.value
                tot_elem = tot_elem.totient_element
                totient_ls.append(tot_val)
            totient_set[data_elem.value] = totient_ls
        self.flat_totient_set = totient_set

    def extract_totient(self):
        if self.flat_totient_set is None:
            self.flatten_totient()
        self.extracted_totient_set = dict()
        for int_key in self.flat_totient_set.keys():
            totient_ls = self.flat_totient_set[int_key]
            ex_totient_ls = []
            ex_int_key = int_key.get_val()
            for tot_elem in totient_ls:
                ex_totient_ls.append(tot_elem.get_val())
            self.extracted_totient_set[ex_int_key] = ex_totient_ls

    def order_totient(self):
        if self.extracted_totient_set is None:
            self.extract_totient()
        self.ordered_int_set = []
        self.ordered_totient_set = []
        self.ordered_totient_time_set = []
        for int_key in self.extracted_totient_set.keys():
            tot_set = self.extracted_totient_set[int_key]
            tot_len = len(tot_set)
            for i in range(0, tot_len):
                self.ordered_int_set.append(int_key)
                self.ordered_totient_set.append(tot_set[i])
                self.ordered_totient_time_set.append(i)
