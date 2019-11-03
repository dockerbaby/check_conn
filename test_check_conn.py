import unittest
import check_conn

class TestCheckConn(unittest.TestCase):

    def test_parse_args(self):
        """
        test_parse_args - verify that function 'parse_args' correctly parses command line arguments 
                          and assigns them to the correct name-value pair
        """
        # Check that parse_args returns correct hostname and port argument values from command line arguments.
        args = check_conn.parse_args('./check_conn.py www.google.com -p 80'.split())
        self.assertEquals(args.hostname, 'www.google.com')
        self.assertEquals(args.port, '80')

        args = check_conn.parse_args('./check_conn.py www.google.com -p 443'.split())
        self.assertEquals(args.hostname, 'www.google.com')
        self.assertEquals(args.port, '443')

        args = check_conn.parse_args('./check_conn.py www.google.com -p "443"'.split())
        self.assertEquals(args.hostname, 'www.google.com')
        self.assertEquals(args.port, '"443"')

        args = check_conn.parse_args('./check_conn.py www.google.com -p 443 234 456 567 hfg alkj'.split())
        self.assertEquals(args.hostname, 'www.google.com')
        self.assertEquals(args.port, '443')
     
        args = check_conn.parse_args('./check_conn.py www.google.com -'.split())
        self.assertEquals(args.hostname, 'www.google.com')
        self.assertEquals(args.port, None)

        args = check_conn.parse_args('./check_conn.py www.google.com -p'.split())
        self.assertEquals(args.hostname, 'www.google.com')
        self.assertEquals(args.port, None)
     
        args = check_conn.parse_args('./check_conn.py www.google.com'.split())
        self.assertEquals(args.hostname, 'www.google.com')
        self.assertEquals(args.port, None)

    
    def test_check_conn(self):
        """
        test_check_conn - verify that function 'check_conn' returns the correct status of a network
                          connection attempt
        """
        # Valid hostnames and valid port numbers
        self.assertEquals(check_conn.check_conn('www.google.com', '80'), 0)
        self.assertEquals(check_conn.check_conn('www.google.com', 80), 0)

        # Valid hostnames and invalid port numbers
        self.assertEquals(check_conn.check_conn('www.google.com', "80."), 1)
        self.assertEquals(check_conn.check_conn('www.google.com', '80.0'), 1)
        self.assertEquals(check_conn.check_conn('www.google.com', 'ssh'), 1)

        # Valid hostnames and port numbers that are accessible.
        self.assertEquals(check_conn.check_conn('www.google.com', "80"), 0)
        self.assertEquals(check_conn.check_conn('www.google.com', '443'), 0)
        self.assertEquals(check_conn.check_conn('www.google.com',  80), 0)

        # Valid hostnames and port numbers that are inaccessible.
        self.assertEquals(check_conn.check_conn('www.google.com', "8080"), 11)
        self.assertEquals(check_conn.check_conn('www.google.com', '22'), 11)
        self.assertEquals(check_conn.check_conn('www.google.com',  9999), 11)

        # Invalid hostnames and port numbers that are inaccessible.
        self.assertEquals(check_conn.check_conn('www.googlekjslkdjflaksdlfjldf.com', '8080'), 1)
        self.assertEquals(check_conn.check_conn('www.google.m', '22'), 1)
        self.assertEquals(check_conn.check_conn('www.google.', '9999'), 1)
        self.assertEquals(check_conn.check_conn('www.goo.cm', '80 ere 321 sdf 432 234'), 1)

    def test_main(self):
        """
        test_main - verify that function 'main' accepts an argument vector of command-line arguments
                    and returns the right value from a network connection attempt.
        """
        # Valid hostnames and port numbers that are accessible.
        self.assertEquals(check_conn.main(['./check_conn.py', 'www.google.com', '-p', '80']), 0)
        self.assertEquals(check_conn.main(['./check_conn.py', 'www.google.com', '-p', "80"]), 0)
        self.assertEquals(check_conn.main('./check_conn.py -p 443 www.google.com'.split()), 0)
        self.assertEquals(check_conn.main('./check_conn.py -p 80 www.google.com'.split()), 0)
        self.assertEquals(check_conn.main('./check_conn.py www.google.com -p 80'.split()), 0)
        self.assertEquals(check_conn.main('./check_conn.py www.google.com -p 80 -p 80'.split()), 0)
        self.assertEquals(check_conn.main('./check_conn.py www.google.com -p 80 ere 321 sdf 432 234'.split()), 0)

        # Valid hostnames and integer port numbers, but that are inaccessible.
        self.assertEquals(check_conn.main('./check_conn.py -p www.google.com -p 80'.split()), 1)
        self.assertEquals(check_conn.main('./check_conn.py -p www.google.com -p 80'.split()), 1)
        self.assertEquals(check_conn.main(['./check_conn.py', 'www.google.com', '-p', '8080']), 1)
        self.assertEquals(check_conn.main('./check_conn.py www.google.com -p 234 ere 321 sdf 432 234'.split()), 1)
        self.assertEquals(check_conn.main('./check_conn.py www.google.com -p 8080 ere 321 sdf 432 234'.split()), 1)
        self.assertEquals(check_conn.main('./check_conn.py -p 8080 www.google.com'.split()), 1)
        self.assertEquals(check_conn.main('./check_conn.py -p 234 556 dfgg www.google.com'.split()), 1)

        # Valid hostnames with invalid port designations.
        self.assertEquals(check_conn.main('./check_conn.py www.google.com'.split()), 1)
        self.assertEquals(check_conn.main(['./check_conn.py', 'www.google.com']), 1)
        self.assertEquals(check_conn.main('./check_conn.py www.google.com -'.split()), 1)
        self.assertEquals(check_conn.main('./check_conn.py www.google.com -p'.split()), 1)
        self.assertEquals(check_conn.main('./check_conn.py www.google.com 80'.split()), 1)
        self.assertEquals(check_conn.main('./check_conn.py www.google.com 22'.split()), 1)
        self.assertEquals(check_conn.main('./check_conn.py www.google.com -p 22'.split()), 1)
        self.assertEquals(check_conn.main('./check_conn.py www.google.com ssh'.split()), 1)
        self.assertEquals(check_conn.main('./check_conn.py www.google.com - ssh'.split()), 1)
        self.assertEquals(check_conn.main('./check_conn.py www.google.com -p ssh'.split()), 1)
        self.assertEquals(check_conn.main('./check_conn.py -p www.google.com'.split()), 1)
        self.assertEquals(check_conn.main('./check_conn.py -p 80.0 www.google.com'.split()), 1)
        self.assertEquals(check_conn.main('./check_conn.py -p "80.0" www.google.com'.split()), 1)
        self.assertEquals(check_conn.main(['./check_conn.py', 'www.google.com', '-p', '"80"']), 1)
       
        # Invalid hostnames with a mixture of valid/invalid port numbers.
        self.assertEquals(check_conn.main(['./check_conn.py']), 1)
        self.assertEquals(check_conn.main('./check_conn.py -'.split()), 1)
        self.assertEquals(check_conn.main('./check_conn.py -p'.split()), 1)
        self.assertEquals(check_conn.main(['./check_conn.py', '-p', '80']), 1)
        self.assertEquals(check_conn.main(['./check_conn.py', '-p', 'ssh']), 1)
        self.assertEquals(check_conn.main('./check_conn.py -p 80 www..com'.split()), 1)
        self.assertEquals(check_conn.main(['./check_conn.py', 'www.googledkjfaljsflkjlskj.com']), 1)
        self.assertEquals(check_conn.main('./check_conn.py -p 80 www.googledkjfaljsflkjlskj.com'.split()), 1)
     
if __name__ == '__main__':
    unittest.main()
