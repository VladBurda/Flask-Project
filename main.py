from flask import Flask, render_template, request, redirect, url_for, session
from program.user import User  
from program.group import Group  

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Mock database
users_db = {
    "test@example.com": User(1, "test@example.com", "password123", "A test user"),
    "john.doe@example.com": User(2, "john.doe@example.com", "securepass", "John Doe"),
    "jane.smith@example.com": User(3, "jane.smith@example.com", "mypassword", "Jane Smith"),
    "alice.wonderland@example.com": User(4, "alice.wonderland@example.com", "alice123", "Alice Wonderland"),
    "bob.builder@example.com": User(5, "bob.builder@example.com", "canwefixit", "Bob Builder"),
}


groups_db = {
    1: Group("Python Developers", "A group for Python enthusiasts", 1, "test@example.com", True),
    2: Group("Flask Users", "All about Flask framework", 2, "test@example.com", True),
}

#Adding Topics to the groups    
groups_db[1].topics = {
    1: "Python basics",
    2: "Python advanced",
    3: "Python libraries",
}

groups_db[2].topics = {
    1: "Flask basics",
    2: "Flask advanced",
    3: "Flask extensions",
}

# Assign groups to the users
users_db["test@example.com"].add_group(groups_db[1])
users_db["test@example.com"].add_group(groups_db[2])
users_db["john.doe@example.com"].add_group(groups_db[2])

#Assgning users to the groups
groups_db[1].add_user("test@example.com")
groups_db[2].add_user("test@example.com")
groups_db[2].add_user("john.doe@example.com")

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = users_db.get(email)

    if user and user.password == password:
        session['user_id'] = user.user_id
        session['email'] = user.email
        return redirect(url_for('main'))
    else:
        return "Invalid credentials. Try again."

@app.route('/main')
def main():
    if 'email' not in session:
        return redirect(url_for('index'))

    user = users_db[session['email']]
    
    # Zamiana listy obiektów Group na słownik {group_id: group}
    user_groups = {group.group_id: group for group in user.groups}

    return render_template('main.html', username=user.username(), groups=user_groups)


def autosplitting_topics(group, topics_to_split):
    lines = topics_to_split.split("\n")
    current_key = None
    current_value = []

    for line in lines:
        parts = line.split(". ", 1)  # Splitting only at first occurrence of ". "
        if len(parts) == 2 and parts[0].isdigit():  
            if current_key is not None:
                group.topics[current_key] = "\n".join(current_value)  # Save previous topic
            current_key = int(parts[0])
            current_value = [parts[1]]
        else:
            if current_key is not None:
                current_value.append(line)  # Append multiline content

    if current_key is not None:
        group.topics[current_key] = "\n".join(current_value)


@app.route('/create_group', methods=['GET', 'POST'])
def create_group():
    if 'email' not in session:
        return redirect(url_for('index'))  # Redirect if not logged in

    if request.method == 'POST':
        group_name = request.form['groupName']
        group_desc = request.form['groupDescription']
        is_private = request.form.get('Status') == 'Active'
        topics_input = request.form.get('addTopics', '').strip()

        # Transform topics on first submit
        if 'preview' in request.form:
            new_group = Group(group_name, group_desc, 0, session['email'], is_private)  # Temporary ID
            autosplitting_topics(new_group, topics_input)
            return render_template(
                'create_group.html',
                group_name=group_name,
                group_desc=group_desc,
                is_private=is_private,
                topics=new_group.topics,  # Send transformed topics
            )            

        # Final creation
        elif 'final_submit' in request.form:
            # Generate unique ID
            new_group_id = len(groups_db) + 1
            new_group = Group(group_name, group_desc, new_group_id, session['email'], is_private)
            groups_db[new_group_id] = new_group

            # Collect modified topics from form fields
            topics = {}
            for key, value in request.form.items():
                if key.startswith("topic_"):
                    topic_number = int(key.replace("topic_", ""))
                    topics[topic_number] = value.strip()

            new_group.topics = topics  # Assign modified topics

            # Add group to user
            user = users_db[session['email']]
            user.add_group(new_group)

            return redirect(url_for('main'))  # Redirect to main page

    return render_template('create_group.html')

@app.route('/group/<int:group_id>', methods=['GET', 'POST'])
def group_details(group_id):
    if 'email' not in session:
        return redirect(url_for('index'))

    user_email = session['email']
    group = groups_db.get(group_id)

    if not group:
        return "Group not found", 404

    if request.method == 'POST':
        # Rezerwacja tematu
        if 'topic_key' in request.form:
            topic_key = int(request.form['topic_key'])

            # Sprawdzenie, czy użytkownik już zarezerwował inny temat
            if user_email in group.reserved_topics.values():
                return "You have already reserved a topic in this group.", 400

            if topic_key in group.topics and topic_key not in group.reserved_topics:
                group.reserved_topics[topic_key] = user_email  # Zapisujemy rezerwację
                print(f"Topic {topic_key} reserved by {user_email}")  # Debug


        # Aktualizacja tematów (dla właściciela)
        if 'update_topics' in request.form and user_email == group.group_owner:
            for key in group.topics.keys():
                topic_key = f"topic_{key}"
                if topic_key in request.form:
                    group.topics[key] = request.form[topic_key]

        # Dodanie nowego tematu (dla właściciela)
        if 'add_topic' in request.form and user_email == group.group_owner:
            new_topic = request.form.get('new_topic')
            if new_topic:
                new_topic_id = max(map(int, group.topics.keys()), default=0) + 1
                group.topics[str(new_topic_id)] = new_topic

    print("Reserved topics:", group.reserved_topics)  # Debugging
    return render_template('group_details.html', group=group)



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
