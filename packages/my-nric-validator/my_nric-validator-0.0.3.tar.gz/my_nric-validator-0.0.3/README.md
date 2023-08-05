# NRIC MY Validator
Python NRIC Malaysia validator

There are 3 function validate_nric, validate_birth_place, and get_birth_date

validate_nric  will be used to validate malaysian NRIC / Mykad Number , it 
will return true if the NRIC malaysia is input correctly.

You just need call the function as the following:

    
    from my_nric import validator


    def example():
        number = "910502-11-5298"
        is_nric_valid = validator.validate_nric(number)
    
        if is_nric_valid:
            print("Is Valid")
        else:
            print("Not Valid NRIC")


#TODO Feature
1. Get the possible birthplace 
2. Get Gender 
3. MyKad Reader function ... __*May be*__