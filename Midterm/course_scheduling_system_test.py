import unittest
from unittest.mock import patch
from unittest.mock import Mock
import course_scheduling_system

class CSSTest(unittest.TestCase):

    def setUp(self):
        self.css = course_scheduling_system.CSS()
        self.new_course = [('Algorithms', 'Monday', 3, 4),('Chinese', 'Monday', 1, 3) ]
        pass

    def test_q1_1(self):
        with patch.object(course_scheduling_system.CSS, 'check_course_exist') as test_exist:
            test_exist.return_value = (True)
            new_course = [('Algorithms', 'Monday', 3, 4)]
            ret = self.css.add_course(new_course[0])
            self.assertTrue(ret)
            cur_course = self.css.get_course_list()
            self.assertEqual(cur_course, new_course)

    def test_q1_2(self):
        with patch.object(course_scheduling_system.CSS, 'check_course_exist') as test_exist:
            test_exist.return_value = (True)
            new_course = [('Algorithms', 'Monday', 3, 4),('Chinese', 'Monday', 1, 3)]
            ret1 = self.css.add_course(new_course[0])
            ret2 = self.css.add_course(new_course[1])
            self.assertTrue(ret1)
            self.assertFalse(ret2)
            cur_course = self.css.get_course_list()
            self.assertNotEqual(cur_course, new_course)

    def test_q1_3(self):
        with patch.object(course_scheduling_system.CSS, 'check_course_exist') as test_exist:
            test_exist.return_value = (False)
            new_course = [('Algorithms', 'Monday', 3, 4)]
            ret1 = self.css.add_course(new_course[0])
            self.assertFalse(ret1)

    def test_q1_4(self):
        with patch.object(course_scheduling_system.CSS, 'check_course_exist') as test_exist:
            test_exist.return_value = (True)
            new_course = [('Algorithms', 'Sunday', 3, 4)]
            with self.assertRaises(TypeError):
                self.css.add_course(new_course[0])

    def test_q1_5(self):
        with patch.object(course_scheduling_system.CSS, 'check_course_exist') as test_exist:
            test_exist.return_value = (True)
            new_course = [('Algorithms', 'Monday', 3, 4),('Chinese', 'Monday', 5, 6),('Math', 'Tuesday', 2, 3)]
            self.css.add_course(new_course[0])
            self.css.add_course(new_course[1])
            self.css.add_course(new_course[2])
            self.css.remove_course(new_course[1])
            courseList = self.css.get_course_list()
            self.assertNotEqual(courseList[0], new_course)
            print(self.css.__str__())
            self.assertEqual(test_exist.call_count,4)
        
if __name__ == "__main__":
    unittest.main()# pragma: no cover