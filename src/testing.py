import unittest
import os
from datetime import date
from q1_time import q1_time
from q2_time import q2_time
from q3_time import q3_time
from q1_memory import q1_memory
from q2_memory import q2_memory
from q3_memory import q3_memory

def getPath(string):
    dir_root = os.path.dirname(os.path.abspath(""))
    path = dir_root + "/data/" + string
    return path

class TestSum(unittest.TestCase):
    # test con un archivo de pocos registros
    def test_q1_time_1(self):
        self.assertListEqual(q1_time(getPath("xample1.json")), [(date(2021, 2, 24), 'PrdeepNain')])
    
    # test con archivo vacio
    def test_q1_time_2(self):
        self.assertListEqual(q1_time(getPath("xample2.json")), [])

    # test con un archivo de pocos registros
    def test_q2_time_1(self):
        self.assertListEqual(q2_time(getPath("xample1.json")), [('🚜', 3), ('🌾', 3), ('💪', 3), ('🤫', 2)])
    
    # test con archivo vacio
    def test_q2_time_2(self):
        self.assertListEqual(q2_time(getPath("xample2.json")), [])

    # test con un archivo de pocos registros
    def test_q3_time_1(self):
        self.assertListEqual(q3_time(getPath("xample1.json")), [('Kisanektamorcha', 3), ('DelhiPolice', 2), ('narendramodi', 1)])

    # test con archivo vacio
    def test_q3_time_2(self):
        self.assertListEqual(q3_time(getPath("xample2.json")), [])
    
    # test con un archivo de pocos registros
    def test_q1_memory_1(self):
        self.assertListEqual(q1_time(getPath("xample1.json")), [(date(2021, 2, 24), 'PrdeepNain')])

    # test con archivo vacio
    def test_q1_memory_2(self):
        self.assertEqual(q1_memory(getPath("xample2.json")), [])

    # test con un archivo de pocos registros
    def test_q2_memory_1(self):
        self.assertListEqual(q2_memory(getPath("xample1.json")), [('🚜', 3), ('🌾', 3), ('💪', 3), ('🤫', 2)])

    # test con archivo vacio
    def test_q2_memory_2(self):
        self.assertEqual(q2_memory(getPath("xample2.json")), [])

    # test con un archivo de pocos registros
    def test_q3_memory_1(self):
        self.assertListEqual(q3_memory(getPath("xample1.json")), [('Kisanektamorcha', 3), ('DelhiPolice', 2), ('narendramodi', 1)])

    # test con archivo vacio
    def test_q3_memory_2(self):
        self.assertEqual(q3_memory(getPath("xample2.json")), [])

if __name__ == '__main__':
    unittest.main()

