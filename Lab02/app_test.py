import unittest
import app
from unittest.mock import Mock, patch

class ApplicationTest(unittest.TestCase):

    def setUp(self):
        # stub
        with patch.object(app.Application, 'get_names') as test_get_names:
            test_get_names.return_value = (['William', 'Oliver', 'Henry', 'Liam'],['William', 'Oliver', 'Henry'])
            self.test_app = app.Application()
        pass
    
    def test_app(self):
        # mock
        # spy
        with patch.object(app.Application, 'get_random_person') as test_get_random:
            test_get_random.side_effect=["William", "Oliver", "Henry", "Liam"]
            next_select = self.test_app.select_next_person()
            self.assertEqual(next_select, "Liam")
            print("{} selected!".format(next_select))

            with patch.object(app.MailSystem, 'write') as test_mail_write, patch.object(app.MailSystem, 'send') as test_mail_send:
                def fake_write(*args, **kwargs):
                    context = 'Congrats, ' + args[0] + '!'
                    return context
                
                def fake_send(*args, **kwargs):
                    print(args[1])

                test_mail_write.side_effect=fake_write
                test_mail_send.side_effect=fake_send
                self.test_app.notify_selected()
                self.assertEqual(test_mail_write.call_count, 4)
                self.assertEqual(test_mail_send.call_count, 4)

                print("\n")
                print(test_mail_write.call_args_list)
                print(test_mail_send.call_args_list)
        pass

if __name__ == "__main__":
    unittest.main()