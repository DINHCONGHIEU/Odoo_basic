e
def test_api_constrains(self):
    
    with self.assertRaises(ValidationError):
        self.env['customer'].create({
                    'name':"Dang",
                    'birthday':'20/10/2023'
                })