import mysql.connector

# --- Global Variables ---
# Set your MySQL credentials here
DB_HOST = "localhost"
DB_USER = "root"  # Replace with your MySQL username
DB_PASSWORD = "521977" # Replace with your MySQL password
DATABASE_NAME = "university"
TABLE_NAME = "student"

student_name = ''
logged = False

# --- Database Setup Functions ---

def get_db_connection():
    """Establishes a connection to the MySQL server."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def setup_database():
    """Creates the 'university' database and the 'student' table if they don't exist."""
    conn = get_db_connection()
    if conn is None:
        return

    cursor = conn.cursor()

    try:
        # Create Database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
        
        # Connect to the new database
        conn.database = DATABASE_NAME
        
        # Create Table
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            name VARCHAR(255) PRIMARY KEY,
            email VARCHAR(255),
            contact VARCHAR(20),
            branch VARCHAR(100),
            enroll VARCHAR(50) UNIQUE,
            year VARCHAR(10),
            password VARCHAR(255) # NOTE: In a real application, NEVER store plain passwords! Use hashing (e.g., bcrypt).
        )
        """
        cursor.execute(create_table_query)
        print(f"Database '{DATABASE_NAME}' and table '{TABLE_NAME}' ready.")

    except mysql.connector.Error as err:
        print(f"Database setup error: {err}")
    finally:
        cursor.close()
        conn.close()

# --- Utility Function to Connect to the Specific Database ---

def connect_to_university():
    """Connects to the 'university' database."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DATABASE_NAME
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to the {DATABASE_NAME} database: {err}")
        return None

# --- Main Application Logic ---

def main():
    # Run setup once before the main loop
    setup_database() 
    
    while True:
        print("\nWelcome to the Student System.")
        print("Choose an option to proceed:")
        print(''' 
        1. Register
        2. Login
        3. Exit
        ''')
        first_choice = input("Enter your choice (1, 2, or 3): ")
        if first_choice == '1':
            register()
        elif first_choice == '2':
            login()
        elif first_choice == '3':
            print("Exiting Student System. Goodbye!")
            break
        else:
            print("Invalid choice.")

def register():
    """Handles student registration and inserts data into the MySQL table."""
    print("\n--- Student Registration ---")
    name = input("Enter your name (used as username): ")
    
    # Check if user already exists
    if get_student_details(name):
        print("A user with this name already exists. Please login or choose another name.")
        return
        
    email = input("Enter your email: ")
    contact = input("Enter your contact number: ")
    branch = input("Enter your branch: ")
    enroll = input("Enter your enrollment number: ")
    year = input("Enter your current study year: ")
    password = input("Enter your password: ")
    confirm_password = input("Confirm your password: ")
    
    if password != confirm_password:
        print("Passwords do not match. Please try again.")
        return register()

    conn = connect_to_university()
    if conn is None:
        return
    
    cursor = conn.cursor()
    
    # SQL INSERT statement
    insert_query = f"""
    INSERT INTO {TABLE_NAME} 
    (name, email, contact, branch, enroll, year, password) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    student_data = (name, email, contact, branch, enroll, year, password)

    try:
        cursor.execute(insert_query, student_data)
        conn.commit()
        
        global logged, student_name
        logged = True
        student_name = name
        
        print("Registration Successful.")
        print(f"Welcome {name}, you are logged in.")
        home()
        
    except mysql.connector.Error as err:
        print(f"Error during registration: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_student_details(name):
    """Retrieves a student's record by name from the MySQL table."""
    conn = connect_to_university()
    if conn is None:
        return None

    cursor = conn.cursor(dictionary=True) # Use dictionary=True to get results as dicts
    
    select_query = f"SELECT * FROM {TABLE_NAME} WHERE name = %s"
    
    try:
        cursor.execute(select_query, (name,))
        student_record = cursor.fetchone()
        return student_record
    except mysql.connector.Error as err:
        print(f"Error retrieving data: {err}")
        return None
    finally:
        cursor.close()
        conn.close()


def login():
    """Handles student login by checking credentials against the MySQL table."""
    print ("\n--- Student Login ---")
    sName = input("Enter your Name: ")
    sPW = input("Enter your Password: ")

    student_record = get_student_details(sName)

    if student_record is None:
        print("Name not found. Please register first.")
        return
    
    # Check password
    if sPW == student_record['password']:
        global logged, student_name
        logged = True
        student_name = sName
        print(f"Welcome {sName}, you are logged in.")
        home()
    else:
        print("Incorrect password. Please try again.")
        
def home():
    """Home page menu."""
    if not logged:
        print("Please login first to access the home page.")
        return

    while logged:
        print("\n--- Home Page ---")
        print(f"Logged in as: {student_name}")
        print("Available options:")
        print(''' 
            1. View Profile
            2. Update Profile
            3. Start Quiz
            4. Logout
        ''')
        choice = input("Enter your choice (1-4): ")
        print()
        
        if choice == '1':
            view_profile()
        elif choice == '2':
            update_profile()
        elif choice == '3':
            start_quiz()
        elif choice == '4':
            logout()
            break
        else:
            print("Invalid choice. Please try again.")


def view_profile():
    """Displays the currently logged-in student's profile details from the database."""
    if not logged:
        print("Please login first to view profile.")
        return

    student_record = get_student_details(student_name)
    
    if student_record:
        print("\n--- Viewing Profile ---")
        # Print all key-value pairs from the dictionary record
        for key, value in student_record.items():
            # Exclude the 'password' for security
            if key != 'password': 
                print(f"{key.replace('_', ' ').title()}: {value}")
        print()
    else:
        print("Could not retrieve profile data.")
    
def update_profile():
    """Allows the logged-in student to update their details in the database."""
    if not logged:
        print("Please login first to update profile.")
        return

    print("\n--- Updating Profile ---")
    print("Enter the new details. Press ENTER to keep the existing value.")
    
    # Get current details to use as defaults
    current_data = get_student_details(student_name)
    if not current_data:
        print("Error: Could not retrieve current profile data.")
        return

    # Prompt for new details, using current data as default
    email = input(f"New Email (current: {current_data['email']}): ") or current_data['email']
    contact = input(f"New Contact Number (current: {current_data['contact']}): ") or current_data['contact']
    branch = input(f"New Branch (current: {current_data['branch']}): ") or current_data['branch']
    enroll = input(f"New Enrollment Number (current: {current_data['enroll']}): ") or current_data['enroll']
    year = input(f"New Current Study Year (current: {current_data['year']}): ") or current_data['year']
    
    new_password = input("Enter NEW password (required for update): ")
    confirm_password = input("Confirm NEW password: ")
    
    if new_password != confirm_password:
        print("Passwords do not match. Update cancelled.")
        return

    conn = connect_to_university()
    if conn is None:
        return

    cursor = conn.cursor()
    
    # SQL UPDATE statement
    update_query = f"""
    UPDATE {TABLE_NAME} SET 
        email = %s, contact = %s, branch = %s, enroll = %s, year = %s, password = %s
    WHERE name = %s
    """
    update_data = (email, contact, branch, enroll, year, new_password, student_name)

    try:
        cursor.execute(update_query, update_data)
        conn.commit()
        
        if cursor.rowcount > 0:
            print("Profile Updated Successfully.")
        else:
            print("No changes were made or user not found.")
            
    except mysql.connector.Error as err:
        print(f"Error updating profile: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
        
def start_quiz():
    """Placeholder for the quiz functionality."""
    if logged:
        # import quizz # Uncomment this if you have a separate quizz.py file
        print("\nStarting Quizzz...")
        import quizz
        print("Starting Quizzz...\n")
        quizz.take_quiz()
        # quizz.take_quiz() # Uncomment this if you have a separate quizz.py file
    else:
        print("Please login first to start quiz.")

def logout():
    """Logs out the current user."""
    global logged, student_name
    if logged:
        logged = False
        print(f"User {student_name} has been logged out successfully.")
        student_name = ''
    else:
        print("You are not logged in.")

if __name__ == '__main__':
    main()