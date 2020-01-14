# Assumptions
## Features

<table>
    <tr>
        <th>Feature</th>
        <th>Assumption(s)</th>
    </tr>
    <tr>
        <td>Ability to login, register if not logged in, and log out</td>
        <td><ul>
            <li> Users are kept logged in on a device, so backend waits for a hash indicating the user is already logged in before listening for a password token to be passed.
        </ul></td>
    </tr>
    <tr>
        <td>Ability to reset password if forgotten it</td>
        <td><ul>
            <li> Password is reset by sending a temporary reset link to the user’s email address.
        </ul></td>
    </tr>
    <tr>
        <td>Ability to see a list of channels</td>
        <td><ul>
            <li> The list of channels only provide the name of each channel, and no other metadata.
        </ul></td>
    </tr>
    <tr>
        <td>Ability to create a channel, join a channel, invite someone else to a channel, and leave a channel</td>
        <td><ul>
            <li>Only one user is added to a channel at a time from the backend.
            <li>Only an authorised user of the channel can invite another user.
            <li>An admin or owner can only remove members from channels
            <li>Admins and owners can archive channels
        </ul></td>
    </tr>
    <tr>
        <td>Within a channel, ability to view all messages, view the members of the channel, and the details of the channel</td>
        <td><ul>
            <li> User will be able to view messages sent in the past, these messages are not stored in their local filesystem but rather loaded in as needed.
            <li> Users will see highlighted new messages, the sender, the time it was sent, and whether it has been edited or deleted
        </ul></td>
    </tr>
    <tr>
        <td>Within a channel, ability to send a message now, or to send a message at a specified time in the future</td>
        <td><ul>
            <li> Users cannot send messages with a time stamp in the past.
        </ul></td>
    </tr>
    <tr>
        <td>Within a channel, ability to edit, remove, pin, unpin, react, or unreact to a message</td>
        <td><ul>
            <li>Only admins and the sender can remove a message
            <li>Only the sender can edit a message
            <li>There will be an indicator to inform that a message has been edited
        </ul></td>
    </tr>
    <tr>
        <td>Ability to view user anyone's user profile, and modify a user's own profile (name, email, handle, and profile photo)</td>
        <td><ul>
            <li>
        </ul></td>
    </tr>
    <tr>
        <td>Ability to search for messages based on a search string</td>
        <td><ul>
            <li>
        </ul></td>
    </tr>
    <tr>
        <td>Ability to modify a user's admin privileges: (MEMBER, ADMIN, OWNER)</td>
        <td><ul>
            <li>Only admins can promote and demote people from being admins
            <li>Only one owner exists in a Slackr workspace, the creator of the workspace, owners cannot be added, removed or changed.
        </ul></td>
    </tr>
    <tr>
        <td>Ability to begin a "standup", which is a 15 minute period where users can send messages that at the end of the period will automatically be collated and summarised to all users</td>
        <td><ul>
            <li> Only admins can start a standup session.
            <li> A standup exists within a channel.
        </ul></td>
    </tr>
</table>

## Functions
<table>
    <tr>
        <th>Function</th>
        <th>Assumption(s)</th>
    </tr>
    <tr>
        <td>auth_login</td>
        <td><ul>
            <li>
        </ul></td>
    </tr>
    <tr>
        <td>auth_logout</td>
        <td><ul>
            <li>
        </ul></td>
    </tr>
    <tr>
        <td>auth_register</td>
        <td><ul>
            <li>Users are logged in immediately after they register
        </ul></td>
    </tr>
    <tr>
        <td>auth_passwordreset_request</td>
        <td><ul>
            <li>
        </ul></td>
    </tr>
    <tr>
        <td>auth_passwordreset_reset</td>
        <td><ul>
            <li>
        </ul></td>
    </tr>
    <tr>
        <td>channel_invite</td>
        <td><ul>
            <li>Any authorised user can invite another user to the private/public channel
            <li> When invited, user b’s token is added to the channel’s authorised users
        </ul></td>
    </tr>
    <tr>
        <td>channel_details</td>
        <td><ul>
            <li>Member details returns a list of user names  in the dictionary
            <li>Any user can CALL for channel details, but only authorised users will be able to access the details - unauthorised users have AccessError
        </ul></td>
    </tr>
    <tr>
        <td>channel_messages</td>
        <td><ul>
            <li>
        </ul></td>
    </tr>
    <tr>
        <td>channel_leave</td>
        <td><ul>
            <li>Once leaving, a user is removed from authorised_users in the channel
            <li>Once leaving, an owner is removed from both owners and authorised_user
            <li>An owner can only leave if there is more than 1 owner.ValueError if a sole owner tries to leave a channel.
        </ul></td>
    </tr>
    <tr>
        <td>channel_join</td>
        <td><ul>
            <li>All users can only join ‘public’ channels, private channels MUST have an invite
            <li>A user is added to the auth_token dictionary key once joined
            <li>If a user is part of the channel, print a notice message but do nothing else
        </ul></td>
    </tr>
    <tr>
        <td>channel_addowner</td>
        <td><ul>
            <li>User_a adds user_b as an owner to channel
            <li>If user_b is not part of the channel, when added, user_b is added as an owner and authorised user of the channel. Channel appears under user_b’s user_channels
        </ul></td>
    </tr>
    <tr>
        <td>channel_removeowner</td>
        <td><ul>
            <li>Owners can remove other owners
            <li>An owner can remove themselves, if there are >1 owners of the channel
            <li>An owner cannot remove themselves if they are the only owner
            <li>Once removed, the owner is still an authorised member of the channel
        </ul></td>
    </tr>
    <tr>
        <td>channels_list</td>
        <td><ul>
            <li>“Authorised user is part of” means that the user is in an authorisation list specific to that channel.
            <li>All users are authorised for public channels.
        </ul></td>
    </tr>
    <tr>
        <td>channels_listall</td>
        <td><ul>
            <li>Lists the channel regardless of whether it is public or private, or if the user is even authorised.
        </ul></td>
    </tr>
    <tr>
        <td>channels_create</td>
        <td><ul>
            <li>A channel has an id, name, is_public, owner_token, and auth_tokens as a dictionary key.
        </ul></td>
    </tr>
    <tr>
        <td>message_sendlater</td>
        <td><ul>
            <li>
        </ul></td>
    </tr>
    <tr>
        <td>message_send</td>
        <td><ul>
            <li>
        </ul></td>
    </tr>
    <tr>
        <td>message_remove</td>
        <td><ul>
            <li>Messages have an is_removed and a u_token key.
            <li>AccessError is not a built-in exception.
        </ul></td>
    </tr>
    <tr>
        <td>message_edit</td>
        <td><ul>
            <li>u_id describes the id of the poster; ie. only the poster has the ability to remove and modify an existing message
            <!-- <li><strong>The specification, “Message with message_ is not a valid message that either 1) is a message sent by the authorised user, or; 2) If the authorised user is an admin, is a any message within a channel that the authorised user has joined” is nonsensical? </strong> (seems to be fixed, this wont be removed unless the writer says so)-->
        </ul></td>
    </tr>
    <tr>
        <td>message_react</td>
        <td><ul>
            <li>Messages have a list key called ‘reacts’
        </ul></td>
    </tr>
    <tr>
        <td>message_unreact</td>
        <td><ul>
            <li>
        </ul></td>
    </tr>
    <tr>
        <td>message_pin</td>
        <td><ul>
            <li>
        </ul></td>
    </tr>
    <tr>
        <td>message_unpin</td>
        <td><ul>
            <li>
        </ul></td>
    </tr>
    <tr>
        <td>user_profile</td>
        <td><ul>
            <li>User email, first name, last name, handle of all users are all visible to other users
            <li>Users have their deafult handle set as "{name_first} {name_last}" after registering
        </ul></td>
    </tr>
    <tr>
        <td>user_profile_setname</td>
        <td><ul>
            <li>User name cannot be empty
            <li>Inputted name does not contain new lines or similar characters
            <li>Handle remains unchanged after name change, even if handle is defaulted to previous name
        </ul></td>
    </tr>
    <tr>
        <td>user_profile_setemail</td>
        <td><ul>
            <li>User cannot set their email to be empty.
            <li>If new email is the same as user's current email, nothing happens
        </ul></td>
    </tr>
    <tr>
        <td>user_profile_sethandle</td>
        <td><ul>
            <li>User handle cannot be empty.
            <li>Inputted handle does not contain new lines or similar characters
            <li>If new handle is the same as user's current handle, nothing happens
        </ul></td>
    </tr>
    <tr>
        <td>user_profiles_uploadphoto</td>
        <td><ul>
            <li>Supplied url must be an image
            <li>Image must be a certain fixed size/aspect ratio
        </ul></td>
    </tr>
    <tr>
        <td>standup_start</td>
        <td><ul>
            <li>Time returned is 15 minutes from when the function is called, and can have an error of up to 2 seconds from the actual time the standup ends
        </ul></td>
    </tr>
    <tr>
        <td>standup_send</td>
        <td><ul>
            <li>There exists a variable with when the latest standup will end.
            <li>Message cannot be empty.
        </ul></td>
    </tr>
    <tr>
        <td>search</td>
        <td><ul>
            <li>There exists a list of valid user id, list of tokens and list of tokens with admin privileges.
        </ul></td>
    </tr>
    <tr>
        <td>admin_userpermission_change</td>
        <td><ul>
            <li>Only one owner exists in Slackr
            <li>First to register is Owner (not just admin)
            <li>Others that register are members, and can be promoted to admin (not owner) by other admins
            <li>Members are not able to set their permission_id = 1 (to member), this will cause an AccessError Exception
            <li>Admins can demote themselves to members
            <li>If admins change their permissions to admin, nothing happens
            <li>No user can change their permissions to owner
        </ul></td>
    </tr>
</table>
