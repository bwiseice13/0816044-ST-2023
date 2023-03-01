import unittest# pragma: no cover
import Students# pragma: no cover

class Test(unittest.TestCase):
    students = Students.Students()# pragma: no cover

    user_name = ['John', 'Mary','Thomas','Jane']# pragma: no cover
    user_id = []# pragma: no cover

    # test case function to check the Students.set_name function
    def test_0_set_name(self):
        #TODO
        print("Start set_name test\n")
        for user in self.user_name:
            result = self.students.set_name(user)
            print(result, user)
            self.assertNotIn(result, self.user_id)
            self.user_id.append(result)
        print("\nFinish set_name test\n")
        pass

    # test case function to check the Students.get_name function
    def test_1_get_name(self):
        #TODO
        print("\nStart get_name test\n")
        print("user_id length =  {}".format(len(self.user_id)))
        print("user_name length =  {}\n".format(len(self.user_name)))
        cnt = 0
        for id in self.user_id:
            result = self.students.get_name(id)
            print("id {i} : {r}".format(r=result, i=id))
            self.assertEqual(result, self.user_name[cnt])
            cnt += 1

        mex = 0
        while mex in self.user_id:
            mex += 1
        print("id {i} : {r}".format(r='There is no such user', i=mex))
        self.assertEqual(self.students.get_name(mex), 'There is no such user')
        print("\nFinish get_name test\n")
        pass
