import sum_function

def main():
    print("Sum Calculator")
    print("---------------")
    
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        
        result = sum_function.add(num1, num2)
        
        print(f"The sum of {num1} and {num2} is: {result}")
        
    except ValueError:
        print("Invalid input. Please enter valid numbers.")

if __name__ == "__main__":
    main()