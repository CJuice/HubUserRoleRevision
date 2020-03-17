"""
Manipulate Hub Community with Python API.
Used originally to manipulate the role of users in the community to make it possible for them to Join External Groups
Created a custom role called MarylandViewer with this ability enabled.
As of 20191119, for default role settings we are only able to choose Publisher or User and not MarylandViewer.
This script can be used to batch update, periodically, the role of new users from User to MarylandViewer

Author: CJuice
Created: 20191119
Revision: 20191209, CJuice, Needed functionality to check for Viewer roles and convert them to MarylandViewer role
20200211, CJuice, Added variable for newly created role called marylandpublisher. Unused at this time, just documenting.
20200213, CJuice, Added a dict for the cryptic account role key to a meaningful english term. Added functionality
    to edit dataframe values to meaningful terms before being printed so that the output is human readable/meaningful
20200302, CJuice, revised print statements in user and viewer loops. Was getting a UnicodeEncodeError on certain
    accounts. Added some intentional encoding and try/except statements to see if that will solve the issue.
20200315, CJuice, revised the search query for users to use the max_users parameter. The process was only getting
    100 by default but we had more than that coming in. Now passing a variable with a high limit to capture all
    users in the categories of interest.
20200317, CJuice, revised the code to include the new SHAViewer role key and to affect the df printout
"""


def main():

    # IMPORTS
    from arcgis.gis import GIS
    import configparser
    import os

    # VARIABLES
    _root_project_path = os.path.dirname(__file__)
    max_number_users = 10000

    # Credentials access and variable creation
    credentials_file = fr"{_root_project_path}\Credentials\Credentials.cfg"
    config_parser = configparser.ConfigParser()
    config_parser.read(credentials_file)
    md_hub_url = config_parser["DEFAULT"]["url"]
    md_hub_admin = config_parser["DEFAULT"]["login"]
    md_hub_pwd = config_parser["DEFAULT"]["password"]

    #   esri keys for their roles in the Hub. Sometimes are intelligible strings and sometimes are not
    maryland_viewer_key = "EuJRbh4M3lBwBRI8"
    maryland_publisher_key = "OIe6FIO92rq2Onxc"
    esri_viewer_key = "iAAAAAAAAAAAAAAA"
    esri_user_key = "org_user"
    esri_admin_key = "org_admin"
    sha_viewer_key = "Arb8zO845H7zLE1Z"
    role_key_to_name_dict = {maryland_viewer_key: "Maryland Viewer", maryland_publisher_key: "Maryland Publisher",
                             esri_viewer_key: "Esri Viewer", esri_user_key: "Esri User", esri_admin_key: "Admin",
                             sha_viewer_key: "SHA Viewer"}

    # FUNCTIONALITY
    # Create a gis connection and get the users in the hub
    gis = GIS(url=md_hub_url, username=md_hub_admin, password=md_hub_pwd)
    users = gis.users

    # Print out a dataframe of roles and the number of accounts/users at that role setting before manipulation
    print("\nBefore:")
    user_role_df = users.counts(type="role", as_df=True)
    user_role_df["key"] = user_role_df["key"].apply(lambda x: role_key_to_name_dict.get(x, x))
    print(user_role_df)

    # Some search options saved for testing and insights. NOTE: .search() returns a max of 100 objects by default
    # print(users.search(role="org_admin", max_users=max_number_users))
    # print(users.search(role="iAAAAAAAAAAAAAAA", max_users=max_number_users)) # Viewer role key
    # print(users.search(role="org_publisher", max_users=max_number_users))
    # print(len(users.search(role="EuJRbh4M3lBwBRI8", max_users=max_number_users)))  # MarylandViewer role key

    # Manipulate the role of community accounts. The default is Role=User
    # NOTE: .search() returns a max of 100 objects default.
    user_role_users = users.search(role=esri_user_key, max_users=max_number_users)
    print(user_role_users)
    viewer_role_users = users.search(role=esri_viewer_key, max_users=max_number_users)
    print(viewer_role_users)

    # The default role is User (ESRI Role). Our MarylandViewer doesn't meet requirements to be populated as choice.
    #   We need to convert User roles to MarylandViewer
    for user in user_role_users:
        try:
            fullName_encoded = (user.fullName).encode(encoding="utf-8")
            role_encoded = (user.role).encode(encoding="utf-8")
            print(f"Viewer: {fullName_encoded}, Role: {role_encoded}")
        except UnicodeEncodeError as uee:
            print(f"UnicodeEncodeError: {uee}")
        result = user.update_role(role=maryland_viewer_key)
        print(f"\tModified: {result}")

    # We do not want a Viewer role to exist so we also need to check and convert Viewer to MarylandViewer
    for viewer in viewer_role_users:
        try:
            fullName_encoded = (viewer.fullName).encode(encoding="utf-8")
            role_encoded = (viewer.role).encode(encoding="utf-8")
            print(f"Viewer: {fullName_encoded}, Role: {role_encoded}")
        except UnicodeEncodeError as uee:
            print(f"UnicodeEncodeError: {uee}")
        result = viewer.update_role(role=maryland_viewer_key)
        print(f"\tModified: {result}")

    # Print out a dataframe of roles and the number of accounts/users at that role setting after manipulation
    print("\nAfter:")
    user_role_df = users.counts(type="role", as_df=True)
    user_role_df["key"] = user_role_df["key"].apply(lambda x: role_key_to_name_dict.get(x, "Unknown, Needs Attention"))
    print(user_role_df)


if __name__ == "__main__":
    main()
