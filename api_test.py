try:
    from app import app
    import unittest
except Exception as e:
    print("Some Modules are missing {} ".format(e))


class FlaskTest(unittest.TestCase):

    # Check for response 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/api/ping")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # check if content is application/JSON
    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/api/ping")
        self.assertEqual(response.content_type, "application/json")

    # check to see if posts are being returned
    def test_api_data(self):
        tester = app.test_client(self)
        response = tester.get("/api/posts?tags=tech")
        self.assertTrue(b'posts' in response.data)


if __name__ == "__main__":
    unittest.main()
