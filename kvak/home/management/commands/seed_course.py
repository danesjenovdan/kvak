from django.core.management.base import BaseCommand
from django.utils.text import slugify
from wagtail.models import Page
from wagtail.rich_text import RichText

from home.models import (
    HomePage,
    CoursesListPage,
    CoursePage,
    ExcerciseCategoryPage,
    ExercisePage,
    BaseMaterialPage,
)


class Command(BaseCommand):
    help = "Create seed course data with realistic programming content"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing course data before creating new',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.clear_existing_data()

        self.stdout.write("Creating seed course data...")
        
        # Get or create HomePage
        home_page = self.get_home_page()
        
        # Create exercise categories
        categories = self.create_categories(home_page)
        
        # Create courses list page
        courses_list = self.create_courses_list(home_page)
        
        # Create courses with exercises and materials
        self.create_courses(courses_list, categories)
        
        self.stdout.write(
            self.style.SUCCESS("Successfully created seed course data!")
        )

    def clear_existing_data(self):
        """Clear existing course-related pages"""
        self.stdout.write("Clearing existing course data...")
        
        # Delete in reverse hierarchy order to avoid constraint issues
        BaseMaterialPage.objects.all().delete()
        ExercisePage.objects.all().delete()
        CoursePage.objects.all().delete()
        CoursesListPage.objects.all().delete()
        ExcerciseCategoryPage.objects.all().delete()
        
        self.stdout.write("Existing data cleared.")

    def get_home_page(self):
        """Get or create HomePage"""
        try:
            return HomePage.objects.first()
        except HomePage.DoesNotExist:
            # If no HomePage exists, create one as child of root
            root = Page.get_first_root_node()
            home_page = HomePage(
                title="Programming Academy",
                intro_text="<p>Welcome to our comprehensive programming courses!</p>",
                courses_description="Learn programming from basics to advanced topics",
                resources_description="Access our extensive learning resources",
            )
            root.add_child(instance=home_page)
            return home_page

    def create_categories(self, home_page):
        """Create exercise categories"""
        categories_data = [
            {
                "title": "Fundamentals",
                "description": "<p>Basic programming concepts and syntax</p>"
            },
            {
                "title": "Data Structures",
                "description": "<p>Arrays, lists, dictionaries, and more complex structures</p>"
            },
            {
                "title": "Algorithms",
                "description": "<p>Problem-solving techniques and algorithmic thinking</p>"
            },
            {
                "title": "Object-Oriented Programming",
                "description": "<p>Classes, objects, inheritance, and design patterns</p>"
            },
        ]
        
        categories = {}
        for cat_data in categories_data:
            category = ExcerciseCategoryPage(
                title=cat_data["title"],
                description=cat_data["description"],
                slug=slugify(cat_data["title"]),
            )
            home_page.add_child(instance=category)
            categories[cat_data["title"]] = category
            self.stdout.write(f"Created category: {cat_data['title']}")
        
        return categories

    def create_courses_list(self, home_page):
        """Create courses list page"""
        courses_list = CoursesListPage(
            title="Programming Courses",
            intro_text="<p>Choose from our selection of comprehensive programming courses designed for all skill levels.</p>",
            slug="courses",
        )
        home_page.add_child(instance=courses_list)
        self.stdout.write("Created courses list page")
        return courses_list

    def create_courses(self, courses_list, categories):
        """Create courses with exercises and materials"""
        courses_data = [
            {
                "title": "Python for Beginners",
                "overview": """
                <p>Learn Python programming from scratch! This comprehensive course covers:</p>
                <ul>
                    <li>Python syntax and basic concepts</li>
                    <li>Data types and variables</li>
                    <li>Control structures and functions</li>
                    <li>File handling and error management</li>
                </ul>
                <p>Perfect for complete beginners with no programming experience.</p>
                """,
                "exercises": [
                    {
                        "title": "Variables and Data Types",
                        "description": "<p>Learn about Python variables, strings, numbers, and basic operations.</p>",
                        "time": 30,
                        "category": "Fundamentals",
                        "order": 1,
                    },
                    {
                        "title": "Control Structures",
                        "description": "<p>Master if statements, loops, and conditional logic in Python.</p>",
                        "time": 45,
                        "category": "Fundamentals", 
                        "order": 2,
                    },
                    {
                        "title": "Functions and Modules",
                        "description": "<p>Create reusable code with functions and organize code with modules.</p>",
                        "time": 60,
                        "category": "Fundamentals",
                        "order": 3,
                    },
                ]
            },
            {
                "title": "JavaScript Web Development",
                "overview": """
                <p>Master modern JavaScript for web development:</p>
                <ul>
                    <li>ES6+ features and modern syntax</li>
                    <li>DOM manipulation and event handling</li>
                    <li>Asynchronous programming with Promises</li>
                    <li>Working with APIs and fetch requests</li>
                </ul>
                <p>Build interactive web applications from the ground up.</p>
                """,
                "exercises": [
                    {
                        "title": "DOM Manipulation",
                        "description": "<p>Learn to dynamically modify web pages using JavaScript.</p>",
                        "time": 40,
                        "category": "Fundamentals",
                        "order": 1,
                    },
                    {
                        "title": "Event Handling",
                        "description": "<p>Handle user interactions and create responsive interfaces.</p>",
                        "time": 35,
                        "category": "Fundamentals",
                        "order": 2,
                    },
                    {
                        "title": "Asynchronous Programming",
                        "description": "<p>Master Promises, async/await, and API interactions.</p>",
                        "time": 50,
                        "category": "Algorithms",
                        "order": 3,
                    },
                    {
                        "title": "Object-Oriented JavaScript",
                        "description": "<p>Learn classes, prototypes, and OOP principles in JavaScript.</p>",
                        "time": 55,
                        "category": "Object-Oriented Programming",
                        "order": 4,
                    },
                ]
            }
        ]

        for course_data in courses_data:
            # Create course
            course = CoursePage(
                title=course_data["title"],
                overview=course_data["overview"],
                slug=slugify(course_data["title"]),
            )
            courses_list.add_child(instance=course)
            self.stdout.write(f"Created course: {course_data['title']}")

            # Create exercises for this course
            for exercise_data in course_data["exercises"]:
                exercise = ExercisePage(
                    title=exercise_data["title"],
                    description=exercise_data["description"],
                    estimated_time=exercise_data["time"],
                    category=categories.get(exercise_data["category"]),
                    order=exercise_data["order"],
                    slug=slugify(exercise_data["title"]),
                )
                course.add_child(instance=exercise)
                self.stdout.write(f"  Created exercise: {exercise_data['title']}")

                # Create material for this exercise
                material = self.create_material_for_exercise(exercise, exercise_data)
                self.stdout.write(f"    Created material: {material.title}")

    def create_material_for_exercise(self, exercise, exercise_data):
        """Create a BaseMaterialPage with questions for an exercise"""
        
        # Material content based on exercise topic
        material_content = {
            "Variables and Data Types": {
                "text": """
                <h2>Python Variables and Data Types</h2>
                <p>In Python, variables are containers for storing data values. Unlike other programming languages, Python has no command for declaring a variable.</p>
                
                <h3>Creating Variables</h3>
                <pre><code>x = 5
name = "John"
is_student = True</code></pre>
                
                <h3>Data Types</h3>
                <ul>
                    <li><strong>int</strong> - Integer numbers (5, -3, 100)</li>
                    <li><strong>float</strong> - Decimal numbers (3.14, -2.5)</li>
                    <li><strong>str</strong> - Text strings ("Hello", 'World')</li>
                    <li><strong>bool</strong> - Boolean values (True, False)</li>
                </ul>
                """,
                "video_url": "https://www.youtube.com/watch?v=example1",
            },
            "Control Structures": {
                "text": """
                <h2>Control Structures in Python</h2>
                <p>Control structures allow you to control the flow of your program's execution.</p>
                
                <h3>If Statements</h3>
                <pre><code>age = 18
if age >= 18:
    print("You can vote!")
else:
    print("Too young to vote")</code></pre>
                
                <h3>Loops</h3>
                <p><strong>For loops:</strong></p>
                <pre><code>for i in range(5):
    print(i)</code></pre>
                
                <p><strong>While loops:</strong></p>
                <pre><code>count = 0
while count < 5:
    print(count)
    count += 1</code></pre>
                """,
                "video_url": "https://www.youtube.com/watch?v=example2",
            },
            "Functions and Modules": {
                "text": """
                <h2>Functions and Modules</h2>
                <p>Functions help you organize and reuse code efficiently.</p>
                
                <h3>Defining Functions</h3>
                <pre><code>def greet(name):
    return f"Hello, {name}!"

message = greet("Alice")
print(message)</code></pre>
                
                <h3>Modules</h3>
                <p>Modules allow you to organize related functions and variables:</p>
                <pre><code>import math
result = math.sqrt(16)  # Returns 4.0</code></pre>
                """,
                "video_url": "https://www.youtube.com/watch?v=example3",
            },
            "DOM Manipulation": {
                "text": """
                <h2>DOM Manipulation with JavaScript</h2>
                <p>The Document Object Model (DOM) allows you to modify web pages dynamically.</p>
                
                <h3>Selecting Elements</h3>
                <pre><code>// Select by ID
const element = document.getElementById('myElement');

// Select by class
const elements = document.getElementsByClassName('myClass');

// Modern selectors
const element = document.querySelector('#myElement');
const elements = document.querySelectorAll('.myClass');</code></pre>
                
                <h3>Modifying Content</h3>
                <pre><code>element.textContent = 'New text';
element.innerHTML = '&lt;strong&gt;Bold text&lt;/strong&gt;';
element.style.color = 'red';</code></pre>
                """,
                "video_url": "https://www.youtube.com/watch?v=example4",
            },
        }
        
        # Get content or use default
        content = material_content.get(exercise_data["title"], {
            "text": f"<h2>{exercise_data['title']}</h2><p>Complete course material coming soon!</p>",
            "video_url": "https://www.youtube.com/watch?v=example",
        })
        
        # Create material
        material = BaseMaterialPage(
            title=f"{exercise_data['title']} - Course Material",
            text=content["text"],
            video_url=content["video_url"],
            slug=slugify(f"{exercise_data['title']}-material"),
        )
        
        # Add questions based on topic
        questions = self.create_questions_for_topic(exercise_data["title"])
        material.questions = questions
        
        exercise.add_child(instance=material)
        return material

    def create_questions_for_topic(self, topic_title):
        """Create questions based on the topic"""
        
        questions_data = {
            "Variables and Data Types": [
                {
                    "type": "multiple_choice_question",
                    "question_text": "<p>Which of the following are valid Python data types? (Select all that apply)</p>",
                    "explanation_text": "<p>Python has several built-in data types including int, float, str, and bool.</p>",
                    "answer_options": [
                        {"option_text": "int", "is_correct": True},
                        {"option_text": "string", "is_correct": False},
                        {"option_text": "float", "is_correct": True},
                        {"option_text": "bool", "is_correct": True},
                        {"option_text": "number", "is_correct": False},
                    ]
                },
                {
                    "type": "one_correct_answer_question", 
                    "question_text": "<p>What will be the output of: <code>print(type(3.14))</code></p>",
                    "explanation_text": "<p>3.14 is a decimal number, so Python treats it as a float type.</p>",
                    "answer_options": [
                        {"option_text": "<class 'int'>", "is_correct": False},
                        {"option_text": "<class 'float'>", "is_correct": True},
                        {"option_text": "<class 'str'>", "is_correct": False},
                        {"option_text": "<class 'decimal'>", "is_correct": False},
                    ]
                },
                {
                    "type": "text_answer_question",
                    "question_text": "<p>Complete the code to create a variable named 'age' with value 25:</p><p><code>___ = 25</code></p>",
                    "explanation_text": "<p>In Python, you simply assign a value to a variable name using the = operator.</p>",
                }
            ],
            "Control Structures": [
                {
                    "type": "one_correct_answer_question",
                    "question_text": "<p>What will this code print?</p><pre><code>x = 10\nif x > 5:\n    print('A')\nelif x > 15:\n    print('B')\nelse:\n    print('C')</code></pre>",
                    "explanation_text": "<p>Since x=10 is greater than 5, the first condition is true and 'A' is printed. The elif is not checked.</p>",
                    "answer_options": [
                        {"option_text": "A", "is_correct": True},
                        {"option_text": "B", "is_correct": False},
                        {"option_text": "C", "is_correct": False},
                        {"option_text": "Nothing", "is_correct": False},
                    ]
                },
                {
                    "type": "order_by_priority_question",
                    "question_text": "<p>Arrange these loop types by how often they are typically used in Python (most common first):</p>",
                    "explanation_text": "<p>For loops are most common for iterating over sequences, while loops for unknown iterations, and do-while doesn't exist in Python.</p>",
                    "priority_options": [
                        {"option_text": "for loop"},
                        {"option_text": "while loop"},
                        {"option_text": "do-while loop"},
                    ]
                }
            ],
            "DOM Manipulation": [
                {
                    "type": "multiple_choice_question",
                    "question_text": "<p>Which methods can be used to select elements from the DOM? (Select all that apply)</p>",
                    "explanation_text": "<p>JavaScript provides several methods to select DOM elements.</p>",
                    "answer_options": [
                        {"option_text": "getElementById", "is_correct": True},
                        {"option_text": "querySelector", "is_correct": True},
                        {"option_text": "getElementByClass", "is_correct": False},
                        {"option_text": "querySelectorAll", "is_correct": True},
                    ]
                },
                {
                    "type": "text_answer_question",
                    "question_text": "<p>What property would you use to change the text content of an element?</p>",
                    "explanation_text": "<p>The textContent property is used to get or set the text content of an element.</p>",
                }
            ],
        }
        
        # Get questions for this topic or return empty list
        topic_questions = questions_data.get(topic_title, [])
        
        # Convert to StreamField format
        questions = []
        for q_data in topic_questions:
            if q_data["type"] == "multiple_choice_question":
                questions.append((
                    "multiple_choice_question",
                    {
                        "question_text": q_data["question_text"],
                        "explanation_text": q_data.get("explanation_text", ""),
                        "answer_options": q_data["answer_options"]
                    }
                ))
            elif q_data["type"] == "one_correct_answer_question":
                questions.append((
                    "one_correct_answer_question",
                    {
                        "question_text": q_data["question_text"],
                        "explanation_text": q_data.get("explanation_text", ""),
                        "answer_options": q_data["answer_options"]
                    }
                ))
            elif q_data["type"] == "text_answer_question":
                questions.append((
                    "text_answer_question",
                    {
                        "question_text": q_data["question_text"],
                        "explanation_text": q_data.get("explanation_text", ""),
                    }
                ))
            elif q_data["type"] == "order_by_priority_question":
                questions.append((
                    "order_by_priority_question",
                    {
                        "question_text": q_data["question_text"],
                        "explanation_text": q_data.get("explanation_text", ""),
                        "priority_options": q_data["priority_options"]
                    }
                ))
        
        return questions