from qc_utils import qcmetric
from unittest import TestCase
from collections import OrderedDict
from io import StringIO
from unittest.mock import patch


STAR_LOG = '''                                 Started job on | Feb 16 23:45:04
                         Started mapping on |   Feb 16 23:49:02
                                Finished on |   Feb 17 00:16:34
   Mapping speed, Million of reads per hour |   115.09

                      Number of input reads |   52815760
                  Average input read length |   202
                                UNIQUE READS:
               Uniquely mapped reads number |   49542908
                    Uniquely mapped reads % |   93.80%
                      Average mapped length |   201.00
                   Number of splices: Total |   20633562
        Number of splices: Annotated (sjdb) |   20453258
                   Number of splices: GT/AG |   20442117
                   Number of splices: GC/AG |   154577
                   Number of splices: AT/AC |   11212
           Number of splices: Non-canonical |   25656
                  Mismatch rate per base, % |   0.30%
                     Deletion rate per base |   0.02%
                    Deletion average length |   1.51
                    Insertion rate per base |   0.01%
                   Insertion average length |   1.37
                         MULTI-MAPPING READS:
    Number of reads mapped to multiple loci |   2218531
         % of reads mapped to multiple loci |   4.20%
    Number of reads mapped to too many loci |   7303
         % of reads mapped to too many loci |   0.01%
                              UNMAPPED READS:
   % of reads unmapped: too many mismatches |   0.00%
             % of reads unmapped: too short |   1.95%
                 % of reads unmapped: other |   0.03%
                              CHIMERIC READS:
                   Number of chimeric reads |   0
                        % of chimeric reads |   0.00%'''


class TestQCMetric(TestCase):
    def test_type_check(self):
        with self.assertRaises(TypeError):
            qcmetric.QCMetric('name', 1)

    def test_get_name(self):
        qc_obj = qcmetric.QCMetric('a', {})
        self.assertEqual(qc_obj.name, 'a')

    def test_get_content(self):
        qc_obj = qcmetric.QCMetric('_', {2: 'a', 1: 'b'})
        self.assertEqual(qc_obj.content, OrderedDict([(1, 'b'), (2, 'a')]))

    def test_less_than(self):
        smaller_obj = qcmetric.QCMetric(1, {})
        bigger_obj = qcmetric.QCMetric(2, {})
        self.assertTrue(smaller_obj < bigger_obj)

    def test_equals(self):
        first_obj = qcmetric.QCMetric('a', {})
        second_obj = qcmetric.QCMetric('a', {'x': 'y'})
        self.assertTrue(first_obj == second_obj)

    def test_repr(self):
        obj = qcmetric.QCMetric('a', {1: 'x'})
        self.assertEqual(obj.__repr__(),
                         "QCMetric('a', OrderedDict([(1, 'x')]))")


class TestQCMetricRecord(TestCase):
    def setUp(self):
        self.obj_a1 = qcmetric.QCMetric('a', {1: 2})
        self.obj_a2 = qcmetric.QCMetric('a', {2: 3})
        self.obj_b = qcmetric.QCMetric('b', {3: 4})
        self.obj_c = qcmetric.QCMetric('c', {1: 2, 3: 4, 5: 6})
        self.obj_d = qcmetric.QCMetric('d', {'a': 'b'})
        self.qc_record = qcmetric.QCMetricRecord()

    def test_init_from_list_not_unique(self):
        metrics = [self.obj_a1, self.obj_a2]
        with self.assertRaises(AssertionError):
            qcmetric.QCMetricRecord(metrics)

    def test_init_from_list_success(self):
        metrics = [self.obj_a1, self.obj_b]
        record = qcmetric.QCMetricRecord(metrics)
        self.assertEqual(record.metrics[0], self.obj_a1)
        self.assertEqual(record.metrics[1], self.obj_b)

    def test_add(self):
        self.assertEqual(len(self.qc_record), 0)
        self.qc_record.add(self.obj_a1)
        self.assertEqual(len(self.qc_record), 1)

    def test_add_all_to_empty(self):
        metrics = [self.obj_a1, self.obj_b]
        self.qc_record.add_all(metrics)
        self.assertEqual(len(self.qc_record), 2)

    def test_add_all_to_nonempty_success(self):
        metrics = [self.obj_a1, self.obj_b]
        record = qcmetric.QCMetricRecord(metrics)
        record.add_all([self.obj_c, self.obj_d])
        self.assertEqual(len(record), 4)

    def test_add_all_failure_because_not_unique(self):
        record = qcmetric.QCMetricRecord([self.obj_a1])
        with self.assertRaises(AssertionError):
            record.add_all([self.obj_b, self.obj_a2])
        self.assertEqual(len(record), 1)

    def test_add_raises_error_when_add_same_twice(self):
        self.qc_record.add(self.obj_a1)
        with self.assertRaises(AssertionError):
            self.qc_record.add(self.obj_a1)

    def test_add_raises_error_when_add_with_same_name(self):
        self.qc_record.add(self.obj_a1)
        with self.assertRaises(AssertionError):
            self.qc_record.add(self.obj_a2)

    def test_to_ordered_dict(self):
        self.qc_record.add(self.obj_a1)
        self.qc_record.add(self.obj_b)
        qc_dict = self.qc_record.to_ordered_dict()
        self.assertEqual(qc_dict, OrderedDict([('a', {1: 2}), ('b', {3: 4})]))

    def test_repr(self):
        metrics = [self.obj_a1, self.obj_b]
        record = qcmetric.QCMetricRecord(metrics)
        self.assertEqual(record.__repr__(),
                         "QCMetricRecord([QCMetric('a', OrderedDict([(1, 2)])), QCMetric('b', OrderedDict([(3, 4)]))])")


class TestParsers(TestCase):

    @patch('qc_utils.qcmetric.open', return_value=StringIO(STAR_LOG))
    def test_parse_starlog(self, mock_open):
        star_log_dict = qcmetric.parse_starlog('path')
        self.assertEqual(len(star_log_dict), 29)
