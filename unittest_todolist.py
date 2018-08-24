from todolist import *
import unittest


class TodoListTest(unittest.TestCase):

    def setUp(self):
        self.model = MVCModel()

    def test1_add_and_test_requestAll(self):
        cur.execute("DELETE FROM TodoList")
        con.commit()
        self.model.add(id=1, work_name="Lap trinh Python", starting_date="2018-08-22", ending_date="2018-08-25", status="Doing")
        result = self.model.requestAll()
        self.assertEqual(1, len(result))
        self.assertEqual(1, result[0][0])
        self.assertEqual("Lap trinh Python", result[0][1])
        self.assertEqual("2018-08-22", result[0][2])
        self.assertEqual("2018-08-25", result[0][3])
        self.assertEqual("Doing", result[0][4])

    def test2_edit(self):
        self.model.edit(id=1, work_name="Lap trinh Django", starting_date="2018-08-20", ending_date="2018-08-30", status="Complete")
        edited = self.model.requestAll()[0]
        self.assertEqual("Lap trinh Django", edited[1])
        self.assertEqual("2018-08-20", edited[2])
        self.assertEqual("2018-08-30", edited[3])
        self.assertEqual("Complete", edited[4])

    def test3_request(self):
        id, name = self.model.request(1, 'WorkName')
        self.assertEqual(name, 'Lap trinh Django')

    def test4_checkId(self):
        result = self.model.checkId(1)
        self.assertTrue(result)

    def test5_delete(self):
        self.model.delete(1)
        self.assertEqual(0, len(self.model.requestAll()))

    def tearDown(self):
        pass
unittest.main()
