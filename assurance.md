#Theme: Increase collaboration and communication between UNSW groups and teams

## Initiative A: Communicate via messages with groups of similar interests (channels)

### Epic 1: Group users into channels

-         As a MEMBER, I want to see more details on a channel, so that I can make a more informed decision about the channels I join.

    -   Given a public channel, or a channel that the user is authorised in, when the member requests details then the member can see the full name of the owners, and all members of the channel and the channel name 

-         As a MEMBER, I want to be able to leave a channel when I want to, so that I am no longer subscribed to old interests.

    -   Each channel the user is part of has a ?Leave Channel? button
    
    -   Given a channel the member is authorised in, when the Leave button is pressed, then the member is removed from the channel.
    
    -   That is, when the Leave button is pressed the member is no longer authorised to message in the channel, until they rejoin / are invited the channel



-         As an OWNER, I want to create channels of my choice so that I can form communities of users with matching interests.

    -   Owner has permission to create a new channel, button is found on dashboard
    
    -   Two input fields: Text box with grey placeholder text (?Name?) and a checkbox labelled ?Private channel?
    
    -   Placeholder text disappears once owner starts typing
    
    -   Button labelled ?Create channel? at bottom of dialogue box
    
    -   Once pressed, a new channel is created with the details provided by the owner, and it appears in the channel list

-         As a MEMBER, I want to be able to search for groups I'm interested in, so that I can discover them more easily.

    -   Channels are listed on the page in alphabetical order

-         As a MEMBER, I want to join communities of my choice, so that I can connect with people of matching interests.

    -   Public channels are listed on the list of channels
    
    -   If member wishes to join a particular public channel, they can join by clicking on a channel
    
    -   Upon doing so, the member is added to the list of channel members

### Epic 2: Communicate with users in a channel

-         As a MEMBER, I want to be retract my quick feedback to a message, so that I can change my stance on it in the future.

    -   With every message, there is a list of ?reacts? that a member can choose
    
    -   Clicking on a ?react? button that is already active will retract that react and provide a visual indicator of that feedback to the message

-         As a MEMBER, I want to provide other users with quick feedback on their message(s), so that I can provide input without cluttering the channel or spending additional time.

    -   With every message, there is a list of ?reacts? that a member can choose

    -   Clicking on a ?react? button will provide a visual indicator of feedback to the message

-         As a MEMBER, I want to schedule a message to be sent to a channel at a particular time in the future, so that I can broadcast information at a suitable time, and when I may not be online.

    -   The message field is placed at the bottom of the page
    
    -   The field contains grey placeholder text (?Write a message?)
    
    -   Placeholder disappears once the user starts typing
    
    -   An option on the search bar allows the member to schedule when the message will be sent
    
    -   The member sets the date and time the message is to be scheduled (Must be after current date time)
    
    -   Once the user submits the message, it is scheduled to be recorded in the channel at the specified time
    
    -   This message is to be displayed at the bottom of the page, above the text field

-         As a MEMBER, I want to send messages into a channel, so that I can share information with the rest of the group.

    -   The message field is placed at the bottom of the page
    
    -   The field contains grey placeholder text (?Write a message?)
    
    -   Placeholder disappears once the user starts typing
    
    -   Once the user submits the message, it is recorded in the channel and is displayed at the bottom of the page, above the text field

-         As a MEMBER, I want to see who else is in a channel, so I am aware of the people in the group and connect with them personally.

    -   A panel with a list of all the users who are a part of the channel is displayed
    
    -   The panel lists users by their chosen handles

-         As a MEMBER, I want to see when messages are sent to a channel, so that I can keep track of the chronology of the discussion.

    -   With every message sent in the channel, a formatted time stamp is displayed at the top left of the message, next to the name of the user who sent it

-         As a MEMBER, I want to view message sent to a channel, so I can stay up to date with the rest of the group.

    -   Messages sent to the channel are displayed in chronological order, with the most recent messages at the bottom, and the older messages towards the top

### Epic 3: Manage messages sent within a channel

-         As an ADMIN, I want to be able to delete any message, so that the discussion in the channel remains on-topic and appropriate.

    -   Each message has an option button located to the right of the message
    
    -   Once clicked, one option is labelled ?Remove message?
    
    -   Once ?Remove message? is clicked, it removes the selected message from the channel?s message history

-         As an ADMIN, I want to emphasise important messages so that members are less likely to miss these critical messages when they are catching up on a discussion.

    -   Each message has an option button located to the right of the message

    -   Once clicked, one option is labelled ?Pin message?
    
    -   Once ?Pin message? is clicked, it is placed in a prominent position on the screen

-         As a MEMBER, I want to remove my messages, so that I can unclutter the channel from irrelevant messages.

    -   Each message that the member has sent has an option button located to the right of the message
    
    -   Once clicked, one option is labelled ?Remove message?
    
    -   Once ?Remove message? is clicked, it removes the selected message from the channel?s message history

-         As a MEMBER, I want to edit messages I have sent, so that I can correct any mistakes I may have made in the message.
    
    -   Each message that the member has sent has an option button located to the right of the message
    
    -   Once clicked, one option is labelled ?Edit message?
    
    -   Once ?Edit message? is clicked, the member is able to adjust and submit a revision
    
    -   The edited message is tagged as ?Edited? in an unobtrusive position

-         As a MEMBER, I want to find old messages quickly, so I can read older discussions without having to scroll excessively.

    -   A search field is located in the interface
    
    -   The field contains a grey placeholder text that says ?Search?
    
    -   The placeholder disappears once the member starts typing
    
    -   Search is performed once the member submits the search query

### Epic 4: Moderating and managing channels

-         As an ADMIN, I want to be able to remove particular members from channels, so that I can moderate the discussion.

    -   As an admin, each channel member in the member panel has an option button located next to them
    
    -   Once clicked, one option is labelled ?Remove member?
    
    -   Once ?Remove member? is clicked, the selected member is removed from the channel and they can no longer take part in the channel?s discussion

-         As an OWNER, I want to be able to archive inactive channels, so that I can keep the workspace updated and uncluttered.

    -   As an owner, each channel in the channel list has an option button located next to it
    
    -   Once clicked, one option is labelled ?Archive channel?
    
    -   Once ?Archive channel? is clicked, the selected channel no longer accepts new messages, new reacts, new pins, or new members
    
    -   The archived channel is still able to be viewed

-         As an OWNER, I want to be able to remove channels, so that I can keep the workspace in accordance with the university policy.

    -   As an owner, each channel in the channel list has an option button located next to it
    
    -   Once clicked, one option is labelled ?Delete channel?
    
    -   Once ?Delete channel? is clicked, the selected channel no longer accepts new messages, new reacts, new pins, or new members
    
    -   The deleted channel no longer appears in the channel list

-         As a MEMBER, I want to invite other users into a channel I am a part of, so that they can join in the discussion.

    -   At the channel header, where the messages are displayed, a button is labelled ?Invite members?
    
    -   Once pressed, a dialogue box appears with one text field
    
    -   Text above the field states ?Invite a member to this channel?
    
    -   Grey placeholder text in the text field states ?User ID?
    
    -   The placeholder text disappears once the member starts typing
    
    -   Once a valid user id is submitted, the invited member becomes a member of the selected channel

## Initiative B: Create and access profile information for members

### Epic 1: Identify each team member uniquely

-         As an ADMIN, I want to identify users by a unique username, so that I can discern users from each other.

    -   Upon creation of an account, each user is assigned a unique profile with a unique ID

-         As a MEMBER, I want others to be able to see my contact details, so that they can contact me privately if they need to.

    -   Clicking on another members profile prompts a text box to appear
    
    -   Inside that text box are the contact details of the selected member, formatted correctly to match the information

-         As a MEMBER, I want to receive email notifications, so that I can stay updated on my channels.

    -   An email is sent to the email provided by the user
    
    -   This email includes a summary of what messages were missed by the member
    
    -   This includes unread pinned messages, mentions and standups

-         As a MEMBER, I want to have a profile photo, so that others can identify me quickly.

    -   New members are given a default profile image
    
    -   In a user settings page, an option is given to upload and change the member?s ?Profile Photo?
    
    -   Once clicked, the member is able upload an image of their choice
    
    -   A ?Save changes? button is located on the bottom of the page
    
    -   Once clicked, the new profile image is saved, and the member?s information is updated

-         As a MEMBER, I want there to be a way to distinguish between users of identical names, so that I communicate with the correct person.

    -   Each member is given a unique ID
    
    -   When a member is clicked in the member list, a text box appears containing information on the member
    
    -   This ID is shown in this text box

-         As a MEMBER, I want to be able to reset my password, so that my account is secure even if I forget my password.

    -   On the login page, there is a ?Forgot password? button
    
    -   Once clicked, the user is redirected to a page where there is a text input field
    
    -   Text input field has grey placeholder text reading ?Enter email?
    
    -   Placeholder text disappears once the user begins to type
    
    -   Once the request is submitted, a unique code is sent to the specified email
    
    -   In a separate reset page, there are two text fields: one has grey placeholder text ?Enter password reset code?, and the other has grey placeholder text ?Enter new password?
    
    -   Both placeholders disappear once the user begins to type
    
    -   If the correct code is submitted, the password is updated for that specific user

-         As a MEMBER, I want to my profile to be secure and only accessible by me, so that my identity is projected.

    -   Upon login, a unique, encoded token is assigned to the user

-         As a MEMBER, I want to have my own profile, so that I can use the workspace under a unique identity.

    -   Upon creation of an account, each user is assigned a unique profile with a unique ID

### Epic 2: Manage roles of other team members

-         As an OWNER, I want to be able to remove administrative privileges from admins, so that I can limit admins to a specific group of people.

    -   As an owner, with each member in the channel who is an administrator, there is an option button located next to them
    
    -   Once clicked, one option is labelled ?Revoke administrator privileges?
    
    -   Once ?Revoke administrator privileges? is clicked, the selected member no longer has the moderating privileges of an administrator

-         As an OWNER, I want to grant administrative privileges to particular members, so that the management of individual channels is decentralised and easier.

    -   As an owner, with each member in the channel, there is an option button located next to them
    
    -   Once clicked, one option is labelled ?Grant administrator privileges?
    
    -   Once ?Grant administrator privileges? is clicked, the selected member is given moderating privileges of an administrator

### Epic 3: Look up other user profiles

-         As a MEMBER, I want to see other users' emails, so that I can contact them privately.

    -   Clicking on another members profile prompts a text box to appear
    
    -   Inside that text box are the contact details of the selected member, formatted correctly to match the information
    
    -   This includes the member?s email

-         As a MEMBER, I want to see other users' profiles and photos so that I can quickly identify them.
    
    -   Clicking on another members profile prompts a text box to appear
    
    -   Inside that text box are the contact details of the selected member, formatted correctly to match the information
    
    -   This includes the user?s profile photo

## Initiative C: Run standups within teams

### Epic 1: Set up and shut down a standup session

-         As an ADMIN, I want to cancel or stop a standup session while it is ongoing, so that I can start it at a more appropriate time if necessary.

    -   As an admin, with each channel, there is an option button located next to them
    
    -   Once clicked, one option is labelled ?Stop standup?
    
    -   Once ?Stop standup? is clicked, the standup session will stop
    
    -   Upon stopping, all channel members are notified of the standup stopping

-         As an ADMIN, I want to start 15 minute asynchronous standup sessions, so that every member is updated with the group progress at once.

    -   As an admin, with each channel, there is an option button located next to them
    
    -   Once clicked, one option is labelled ?Begin standup?
    
    -   Once ?Begin standup? is clicked, a 15 minute asynchronous standup session begins in the specified channel
    
    -   Upon starting, all channel members are notified of the standup beginning

### Epic 2: Participate in a standup session

-         As a MEMBER, I want to be able to review my standup messages, so that I can make changes since the time I sent the message.

    -   As a part of a standup, messages that a member sends will be able to be seen by that specific member
    
    -   Each message that the member has sent has an option button located to the right of the message
    
    -   Once clicked, one option is labelled ?Edit message?
    
    -   Once ?Edit message? is clicked, the member is able to adjust and submit a revision
    
    -   The edited message is tagged as ?Edited? in an unobtrusive position

-         As a MEMBER, I want to send normal messages during standup, so that discussions can keep on going.

    -   The message field is placed at the bottom of the page
    
    -   If a standup is in session, the member has a checkbox option to send their message as part of a standup
    
    -   The field contains grey placeholder text (?Write a message?)
    
    -   Placeholder disappears once the user starts typing
    
    -   If the checkbox is not checked, the message will sent as normal and not part of the standup
    
    -   Once the user submits the message, it is recorded in the channel and is displayed at the bottom of the page, above the text field

-         As a MEMBER, I want to send standup messages during standup, so that I can update the group on my progress.

    -   The message field is placed at the bottom of the page
    
    -   If a standup is in session, the member has a checkbox option to send their message as part of a standup
    
    -   The field contains grey placeholder text (?Write a message?)
    
    -   Placeholder disappears once the user starts typing
    
    -   If the checkbox is checked, the message will be queued in the standup and will be visible to the sender only

### Epic 3: Collate stand-up messages 

-         As a MEMBER, I want to see the standup summary at the end, so that I am aware of everyone else's progress.

    -   Once the 15-minute standup session completes, a message is sent in the channel that the standup began in
    
    -   All the messages that were queued as a part of the standup are collated in a single message
    
    -   This message is sent in the specified channel and is seen by all channel members

# Strategies and Tools 
## Some strategies we implemented:
1. Peer programming, for quick real-time edits. For more details, see teamwork.md 

2. Splitting the code into modules, made it manageable for members to attempt the
task and also gave members a better understanding of their own section, i.e. 
we were able to specialise in different areas and improve the total quality. 

## Some tools we implemented: 
1. Pylint - Used to keep consistent style across all our code. Also was easy to 
implement with one-two members running over the code and the other members in 
real-time review. 

2. Pytests - A simple way to test the functionality and effectiveness of code. 
It is faster than trying to implement testing on the front end, as well as 
telling us quickly and specifically where the errors would occur. This tool also
helped us achieve more logically correct code. 

3. API Clients - Before connecting to the front-end, we were able to tests a few
simple function outputs etc. with API clients like Postman and Insomnia. This 
also gave more accurate pinpointing of what errors were occuring when the front-end
broke down. 

4. Python3-coverage - Shows us what parts of our codes were being used, and 
what paths were not being used. Using this tool we could find out if we had 
any logical flaws or were not covering areas of code that may potentially
damage the program.