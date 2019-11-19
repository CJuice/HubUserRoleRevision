"""
Manipulate Hub Community with Python API.
Used originally to manipulate the role of users in the community to make it possible for them to Join External Groups
Created a custom role called MarylandViewer with this ability enabled.
As of 20191119, for default role settings we are only able to choose Publisher or User and not MarylandViewer.
This script can be used to batch update, periodically, the role of new users from User to MarylandViewer

Author: CJuice
Created: 20191119
Revision:

"""


def main():

    # IMPORTS
    from arcgis.gis import GIS
    import configparser
    import os

    # VARIABLES
    _root_project_path = os.path.dirname(__file__)

    # Credentials access and variable creation
    credentials_file = fr"{_root_project_path}\Credentials\Credentials.cfg"
    config_parser = configparser.ConfigParser()
    config_parser.read(credentials_file)
    md_hub_url = config_parser["DEFAULT"]["url"]
    md_hub_admin = config_parser["DEFAULT"]["login"]
    md_hub_pwd = config_parser["DEFAULT"]["password"]

    #   esri keys for their roles in the Hub. Sometimes are intelligible strings and sometimes are not
    maryland_viewer_key = "EuJRbh4M3lBwBRI8"
    esri_viewer_key = "iAAAAAAAAAAAAAAA"
    esri_user_key = "org_user"

    # FUNCTIONALITY
    # Create a gis connection and get the users in the hub
    gis = GIS(url=md_hub_url, username=md_hub_admin, password=md_hub_pwd)
    users = gis.users

    # Print out a dataframe of roles and the number of accounts/users at that role setting before manipulation
    print("\nBefore:")
    user_role_df = users.counts(type="role", as_df=True)
    print(user_role_df)

    # Some search options saved for testing and insights
    # print(users.search(role="org_admin"))
    # print(users.search(role="iAAAAAAAAAAAAAAA")) # Viewer role key
    # print(users.search(role="org_publisher"))
    # print(users.search(role="EuJRbh4M3lBwBRI8"))  # MarylandViewer role key

    # Manipulate the role of community accounts
    viewer_role_users = users.search(role=esri_user_key)
    for viewer in viewer_role_users:
        print(f"Viewer: {viewer.fullName}, Role: {viewer.role}")
        result = viewer.update_role(role=maryland_viewer_key)
        print(f"\tModified: {result}")

    # Print out a dataframe of roles and the number of accounts/users at that role setting after manipulation
    print("\nAfter:")
    user_role_df = users.counts(type="role", as_df=True)
    print(user_role_df)


if __name__ == "__main__":
    main()