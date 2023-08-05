Managing Users and Groups
=========================
|

The SDK allows you to manage users and groups for your organization including creating new groups, inviting users,
activating or deactivating existing users, and adding users to groups.

The SDK is designed to mirror the DataOps Platform UI. This section will show references and examples of how certain
actions are taken in the UI, followed the equivalent actions in the SDK.

Retrieving Existing Users
~~~~~~~~~~~~~~~~~~~~~~~~~

In the UI of a DataOps Platform Organization, you can check the existing users as seen in the below screenshot:

.. image:: ../../_static/images/manage/users_and_groups/users_list.png

|
Existing users in your DataOps Platform organization are stored in the ``users`` attribute of the
:py:class:`streamsets.sdk.ControlHub` object you've instantiated. You can further filter the list of available users by
specifying items like ``id``, ``email_address``, or ``status``:

.. code-block:: python

    # Get all users belonging to current organization
    sch.users

    # Get a particular user
    sch.users.get(email_address='mitch@streamsets.com')

    # Get all currently deactivated users
    sch.users.get_all(status='DEACTIVATED')

**Output:**

.. code-block:: python

    # sch.users
    [<User (email_address=kramer@streamsets.com, display_name=, status=DEACTIVATED, last_modified_on=1651171728277)>,
    <User (email_address=mitch@streamsets.com, display_name=Mitch Test, status=ACTIVE, last_modified_on=1650917674930)>]

    # sch.users.get(email_address='mitch@streamsets.com')
    <User (email_address=mitch@streamsets.com, display_name=Mitch Test, status=ACTIVE, last_modified_on=1650917674930)>

    # sch.users.get_all(status='DEACTIVATED')
    [<User (email_address=kramer@streamsets.com, display_name=, status=DEACTIVATED, last_modified_on=1651171728277)>]

Inviting Users
~~~~~~~~~~~~~~
.. _inviting_users:

Adding users is accomplished in the same section of the UI as seen above by using the 'Add New User' button, shown
below:

.. image:: ../../_static/images/manage/users_and_groups/add_new_user.png

|
Selecting 'Add New User' presents a prompt for filling in the details for the user in question, such as email address,
group membership, and the roles for the user:

.. image:: ../../_static/images/manage/users_and_groups/invite_user_details.png

|
The steps to add and invite a new user in the SDK are quite similar, requiring that you create a :py:class:`streamsets.sdk.sch_models.User`
object, specify an email address, and add any group membership or user roles before inviting the user.

To invite and add a new user to the DataOps Platform using the SDK, you first need to create a
:py:class:`streamsets.sdk.sch_models.User` instance via the :py:class:`streamsets.sdk.sch_models.UserBuilder` class -
which is retrieved from the :py:meth:`streamsets.sdk.ControlHub.get_user_builder` method. Once you've successfully built
the user and updated attributes you wish to set, pass the user object to the :py:meth`streamsets.sdk.ControlHub.invite_user`
method:

.. code-block:: python

    user_builder = sch.get_user_builder()
    user = user_builder.build(email_address='johndeer@test.com')
    user.roles = ['Connection Editor', 'Connection User', 'Topology Editor', 'Topology User']
    # Add user to three groups that exist in the organization: all, beta-testers, pipeline operators
    user.groups = ['all', 'beta-testers', 'pipeline operators']
    response = sch.invite_user(user)

.. note::
  The :py:meth:`streamsets.sdk.ControlHub.invite_user` method will automatically update the invited user's in-memory
  representation, including adding the user's ``id``, ``roles``, and ``groups``.

Updating An Existing User
~~~~~~~~~~~~~~~~~~~~~~~~~
.. _updating_users:

Updating an existing user in the UI is done by expanding the user's details, making necessary changes to attributes like
``roles`` or ``groups``, and saving the changes:

.. image:: ../../_static/images/manage/users_and_groups/update_user_details.png

|
It is also possible to update a user's attributes, like ``roles`` or ``groups``, from the SDK. Simply retrieve the user
you wish to update, modify the desired attribute(s), and then pass the user object to the :py:meth:`streamsets.sdk.ControlHub.update_user()`
method:

.. code-block:: python

    user = sch.users.get(email_address='mitch@streamsets.com')
    # Set the user's roles to be the following
    user.roles = ['Engine Administrator', 'Job Operator', 'Pipeline Editor', 'Deployment Manager']
    # Add the user to two groups
    user.groups = ['new-group', 'updated group']
    response = sch.update_user(user)

Activating or Deactivating Users
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Users can be activated or deactivated as needed for your organization. The activation and deactivation methods in the
SDK can handle multiple users at once, or a single user at a time.

Activating a User
-----------------

In the UI, activation of users is done by selecting the user(s) you wish to activate and using the 'Activate'
button:

.. image:: ../../_static/images/manage/users_and_groups/activate_user.png

|
In the SDK, activation requires a similar set of steps. You will first need to retrieve the user(s) you wish to activate
from your DataOps Platform organization and pass them to the :py:meth:`streamsets.sdk.ControlHub.activate_user` method.
This could be a list of several users that all need to be activated at once, or just a single user by itself:

.. code-block:: python

    # Activate single user
    user = sch.users.get(email_address='kramer@streamsets.com')
    sch.activate_user(user)

    # Activate multiple users
    users = sch.users.get_all(status='DEACTIVATED')
    sch.activate_user(*users)

Deactivating a User
-------------------

Similarly, deactivation of users in the UI is also handled by selecting the user(s) you wish to deactivate and using
the 'Deactivate' button:

.. image:: ../../_static/images/manage/users_and_groups/deactivate_user.png

|
You will first need to retrieve the user(s) you wish to deactivate from your DataOps Platform organization and pass them
to the :py:meth:`streamsets.sdk.ControlHub.deactivate_user` method. Again, this could be a list of several users that
all need to be activated or just a single user by itself:

.. code-block:: python

    # Deactivate single user
    user = sch.users.get(email_address='mitch@streamsets.com')
    sch.deactivate_user(user)

    # Deactivate multiple users
    users = sch.users.get_all(status='ACTIVE')
    sch.activate_user(*users)

Deleting Users
~~~~~~~~~~~~~~

Users can also be deleted from your organization as needed. This will permanently remove the user from your organization,
including the user's email address.

In the UI, deletion is accomplished by selecting the user(s) that need to be deleted and using the the 'Delete' button:

.. image:: ../../_static/images/manage/users_and_groups/delete_user.png

|
You can use the SDK to delete a single user, or multiple users at once. You will need to retrieve the user(s)
you want to delete from your organization, and then pass them into the :py:meth:`streamsets.sdk.ControlHub.delete_user`
method. You can also specify if you need to deactivate the user as well via the optional ``deactivate`` parameter (which
defaults to ``False``):

.. code-block:: python

    # Deactivate and delete a single user
    user = sch.users.get(email_address='kramer@streamsets.com')
    sch.delete_user(user, deactivate=True)

    # Delete multiple users
    users = sch.users.get_all(status='DEACTIVATED')
    sch.delete_user(*users)

Bringing It All Together
~~~~~~~~~~~~~~~~~~~~~~~~

The complete scripts from this section can be found below. Commands that only served to verify some output from the
example have been removed.

.. code-block:: python

    # ---- Retrieving Existing Users ----
    # Get a particular user
    sch.users.get(email_address='mitch@streamsets.com')
    # Get all currently deactivated users
    sch.users.get_all(status='DEACTIVATED')

    # ---- Adding Users ----
    user_builder = sch.get_user_builder()
    user = user_builder.build(email_address='johndeer@test.com')
    user.roles = ['Connection Editor', 'Connection User', 'Topology Editor', 'Topology User']
    # Add user to three groups that exist in the organization: all, beta-testers, pipeline operators
    user.groups = ['all', 'beta-testers', 'pipeline operators']
    response = sch.invite_user(user)

    # ---- Updating An Existing User ----
    user = sch.users.get(email_address='mitch@streamsets.com')
    # Set the user's roles to be the following
    user.roles = ['Engine Administrator', 'Job Operator', 'Pipeline Editor', 'Deployment Manager']
    # Add the user to two groups
    user.groups = ['new-group', 'updated group']
    response = sch.update_user(user)

    # ---- Activating or Deactivating Users ----
    # Activate single user
    user = sch.users.get(email_address='kramer@streamsets.com')
    sch.activate_user(user)
    # Activate multiple users
    users = sch.users.get_all(status='DEACTIVATED')
    sch.activate_user(*users)

    # Deactivate single user
    user = sch.users.get(email_address='mitch@streamsets.com')
    sch.deactivate_user(user)
    # Deactivate multiple users
    users = sch.users.get_all(status='ACTIVE')
    sch.activate_user(*users)

    # ---- Deleting Users ----
    # Deactivate and delete a single user
    user = sch.users.get(email_address='kramer@streamsets.com')
    sch.delete_user(user, deactivate=True)
    # Delete multiple users
    users = sch.users.get_all(status='DEACTIVATED')
    sch.delete_user(*users)
