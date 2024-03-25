def prompt_test_task(learning_material):
    return f"Прочитай файл {learning_material} і придумай по одному новому завданню з рівнем easy, middle," \
             f"hard, нічого зайвого не писатию. Завдання мають бути унікальними." \
             f"Рівень постав у кінці строчки. Написати тільки ці три строчки і все в такому ж форматі. Кожне питання"\
             f"з нової строчки. Всього три строчки! Можеш додавати інщі теми але тільки по мові програмування python" \
             f"і в такому самому форматі як у файлі. Не використовуй коми"


def prompt_code_task(learning_material):
    return f"Прочитай файл {learning_material} і придумай по одному новому завданню з рівнем easy, middle," \
           f"hard, нічого зайвого не писатию. Завдання мають бути унікальними. Рівень постав у кінці строчки. Написати"\
           f"тільки ці три строчки і все в такому ж форматі. Кожне питання з нової строчки. Всього три строчки! Можеш"\
           f"додавати інщі теми але тільки по мові програмування python і в такому самому форматі як у файлі. Зверни"\
           f"увагу що кожне поле виділено подвійними кавичками"


def prompt_lessons(learning_material):
    return f"Прочитай файл {learning_material}, в ньому знаходиться три приклади уроків, напиши схожий урок"\
           f"на тему по програмуванню мови python. Уроки мають бути унікальними. free постав у кінці строчки як в"\
           f"прикладах. Написати в такому ж форматі, щоб можна було легко зберегти в csv файл.  Зверни увагу що кожне"\
           f"поле виділено подвійними кавичками"


ai_test_tasks_prompt = (f"Number,Topic,Question,Var1,Var2,Var3,Right_answer,Level_relation \n"
                        f"'1', 'Functions What does the print() function do?', 'Returns the number of elements in the"
                        f"collection.', 'Outputs a message to the console.', 'Changes the weather to sunny.',"
                        f"'Outputs a message to the console.', 'easy'"
                        f"'2','Functions,What is a lambda function in Python?','This is a function that is called"
                        f"when an error occurs.','This is a function that is performed automatically when the program"
                        f"starts.','This is an anonymous function that can be declared without a name and is used for"
                        f"short calculations.','This is an anonymous function that can be declared without a name and"
                        f"is used for short calculations.','middle'"
                        f"3','Rows,How can you convert a string to a list in Python?','By applying the split() method"
                        f"on a string.','By applying the convert() method on a string.','By applying the to_list()"
                        f"method on a string.','hard'")


ai_code_tasks_prompt = (f"""Number,Topic,Question,Var1,Var2,Var3,Right_answer,Level_relation \n"""
                        
                        f"""1,Looping,"<code># Task: Fill in the blank to iterate through the string and print each
                        character.
                        input_str  =  ""Python""
                        for _____ in input_str:
                            print(_____)</code>","char, input_str","char, char","input_str, char","char, char",easy
                        """
                                                
                        f"""2,Functions,"<code>def count_vowels(input_str):
                            vowels  =  ""aeiouAEIOU""
                            count  =  0
                            for char in input_str:
                                if char in _____:
                                    Count +=  1
                            return count
                        
                        # Test the function with the provided string
                        input_string  =  ""Hello, how are you?""
                        result  =  count_vowels(input_string)
                        print(result) </code> # Output should be 7
                        Fill in the blank with the correct variable to find the number of vowels in the string.",char,
                        input_string,vowels,vowels,middle
                        """
                        
                        f"""3,Functions,"<code>def count_vowels(input_str):
                            vowels  =  ""aeiouAEIOU""
                            count  =  0
                            for char in input_str:
                                if char in _____:
                                    Count +=  1
                            return count
                        
                        # Test the function with the provided string
                        input_string  =  ""Hello, how are you?""
                        result  =  count_vowels(input_string)
                        print(result) </code> # Output should be 7
                        Fill in the blank with the correct variable to find the number of vowels in the string.",char,
                        input_string,vowels,vowels,middle
                        """)


ai_lesson_tasks_prompt = (f"""Number,Topic,Item,Description,text,status \n"
                        11,Strings and lists,Lists and Operations on Them,"In this lesson, we will continue our
                        exploration of lists in Python. We'll learn about various operations that can be performed on
                        lists, such as appending, removing, and sorting elements.","Appending Elements to a List:
                        
                        You can add elements to the end of a list using the append() method.
                        
                        <code>
                        fruits = ['apple', 'banana', 'orange']
                        
                        fruits.append('grape')
                        print(fruits)  # Output: ['apple', 'banana', 'orange', 'grape']
                        </code>
                        
                        Inserting Elements at a Specific Position:
                        
                        You can insert elements at a specific position in the list using the insert() method.
                        
                        <code>
                        fruits = ['apple', 'banana', 'orange']
                        
                        fruits.insert(1, 'grape')
                        print(fruits)  # Output: ['apple', 'grape', 'banana', 'orange']
                        </code>
                        Removing Elements from a List:
                        
                        You can remove elements from a list using various methods like remove() and pop().
                        
                        <code>
                        fruits = ['apple', 'banana', 'orange']
                        
                        fruits.remove('banana')
                        print(fruits)  # Output: ['apple', 'orange']
                        
                        popped_fruit = fruits.pop()
                        print(popped_fruit)  # Output: 'orange'
                        print(fruits)       # Output: ['apple']
                        </code>
                        Checking the Existence of an Element:
                        
                        You can check if an element exists in a list using the in keyword.
                        
                        <code>
                        fruits = ['apple', 'banana', 'orange']
                        
                        print('apple' in fruits)    # Output: True
                        print('grape' in fruits)    # Output: False
                        </code>
                        Sorting a List:
                        
                        You can sort a list using the sort() method, which arranges the elements in ascending order.
                        
                        <code>
                        numbers = [5, 2, 8, 3, 1]
                        
                        numbers.sort()
                        print(numbers)  # Output: [1, 2, 3, 5, 8]
                        </code>
                        To sort in descending order, you can use the reverse parameter.
                        
                        <code>
                        numbers = [5, 2, 8, 3, 1]
                        
                        numbers.sort(reverse=True)
                        print(numbers)  # Output: [8, 5, 3, 2, 1]
                        </code>
                        Copying Lists:
                        
                        Be cautious when copying lists, as using the assignment operator = does not create a new list
                        but rather creates a reference to the original list.
                        
                        <code>
                        fruits = ['apple', 'banana', 'orange']
                        fruits_copy = fruits  # This creates a reference, not a new list
                        
                        fruits_copy.append('grape')
                        print(fruits)       # Output: ['apple', 'banana', 'orange', 'grape']
                        
                        # To create a new independent copy, use the slice operator[:]
                        fruits = ['apple', 'banana', 'orange']
                        fruits_copy = fruits[:]
                        
                        fruits_copy.append('grape')
                        print(fruits)       # Output: ['apple', 'banana', 'orange']
                        </code>
                        Conclusion:
                        
                        In this lesson, we continued our exploration of lists in Python. We learned how to perform
                        various operations on lists, such as appending, inserting, removing, checking the existence
                        of elements, sorting, and copying. Lists are versatile data structures that allow us to store
                        and manipulate collections of items. In the next lesson, we will explore list slices and list
                        comparison operators, enabling us to work with specific subsets of lists and make comparisons
                        between lists.",free11,Strings and lists,Lists and Operations on Them,"In this lesson, we will
                        continue our exploration of lists in Python. We'll learn about various operations that can be
                        performed on lists, such as appending, removing, and sorting elements.","Appending Elements to
                        a List:
                        
                        You can add elements to the end of a list using the append() method.
                        
                        <code>
                        fruits = ['apple', 'banana', 'orange']
                        
                        fruits.append('grape')
                        print(fruits)  # Output: ['apple', 'banana', 'orange', 'grape']
                        </code>
                        
                        Inserting Elements at a Specific Position:
                        
                        You can insert elements at a specific position in the list using the insert() method.
                        
                        <code>
                        fruits = ['apple', 'banana', 'orange']
                        
                        fruits.insert(1, 'grape')
                        print(fruits)  # Output: ['apple', 'grape', 'banana', 'orange']
                        </code>
                        Removing Elements from a List:
                        
                        You can remove elements from a list using various methods like remove() and pop().
                        
                        <code>
                        fruits = ['apple', 'banana', 'orange']
                        
                        fruits.remove('banana')
                        print(fruits)  # Output: ['apple', 'orange']
                        
                        popped_fruit = fruits.pop()
                        print(popped_fruit)  # Output: 'orange'
                        print(fruits)       # Output: ['apple']
                        </code>
                        Checking the Existence of an Element:
                        
                        You can check if an element exists in a list using the in keyword.
                        
                        <code>
                        fruits = ['apple', 'banana', 'orange']
                        
                        print('apple' in fruits)    # Output: True
                        print('grape' in fruits)    # Output: False
                        </code>
                        Sorting a List:
                        
                        You can sort a list using the sort() method, which arranges the elements in ascending order.
                        
                        <code>
                        numbers = [5, 2, 8, 3, 1]
                        
                        numbers.sort()
                        print(numbers)  # Output: [1, 2, 3, 5, 8]
                        </code>
                        To sort in descending order, you can use the reverse parameter.
                        
                        <code>
                        numbers = [5, 2, 8, 3, 1]
                        
                        numbers.sort(reverse=True)
                        print(numbers)  # Output: [8, 5, 3, 2, 1]
                        </code>
                        Copying Lists:
                        
                        Be cautious when copying lists, as using the assignment operator = does not create a new list
                        but rather creates a reference to the original list.
                        
                        <code>
                        fruits = ['apple', 'banana', 'orange']
                        fruits_copy = fruits  # This creates a reference, not a new list
                        
                        fruits_copy.append('grape')
                        print(fruits)       # Output: ['apple', 'banana', 'orange', 'grape']
                        
                        # To create a new independent copy, use the slice operator[:]
                        fruits = ['apple', 'banana', 'orange']
                        fruits_copy = fruits[:]
                        
                        fruits_copy.append('grape')
                        print(fruits)       # Output: ['apple', 'banana', 'orange']
                        </code>
                        Conclusion:
                        
                        In this lesson, we continued our exploration of lists in Python. We learned how to perform
                        various operations on lists, such as appending, inserting, removing, checking the existence of
                        elements, sorting, and copying. Lists are versatile data structures that allow us to store and
                        manipulate collections of items. In the next lesson, we will explore list slices and list
                        comparison operators, enabling us to work with specific subsets of lists and make comparisons
                        between lists.",free""")
