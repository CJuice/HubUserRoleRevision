"""
Manipulate Hub Community with Python API.
Used originally to manipulate the role of users in the community to make it possible for them to Join External Groups

"""


def main():

    # IMPORTS
    from arcgis.gis import GIS
    import configparser

    # VARIABLES
    credentials_file = r"Credentials\Credentials.cfg"
    config_parser = configparser.ConfigParser()
    config_parser.read(credentials_file)
    md_hub_url = config_parser["DEFAULT"]["url"]
    md_hub_admin = config_parser["DEFAULT"]["login"]
    md_hub_pwd = config_parser["DEFAULT"]["password"]
    maryland_viewer_key = "EuJRbh4M3lBwBRI8"
    esri_viewer_key = "iAAAAAAAAAAAAAAA"
    esri_user_key = "org_user"

    # FUNCTIONS

    # FUNCTIONALITY
    gis = GIS(url=md_hub_url, username=md_hub_admin, password=md_hub_pwd)
    users = gis.users

    print("\nBefore manipulation:")
    user_role_df = users.counts(type="role", as_df=True)
    print(user_role_df)

    # print(users.search(role="org_admin"))
    # print(users.search(role="iAAAAAAAAAAAAAAA")) # Viewer role key
    # print(users.search(role="org_publisher"))
    # print(users.search(role="EuJRbh4M3lBwBRI8"))  # MarylandViewer role key

    # Manipulate the role of community accounts
    if True:
        viewer_role_users = users.search(role=esri_user_key)
        for viewer in viewer_role_users:
            print(f"Viewer: {viewer.fullName}, Role: {viewer.role}")
            result = viewer.update_role(role=maryland_viewer_key)
            print(f"\tModified: {result}")

    print("\nAfter manipulation:")
    user_role_df = users.counts(type="role", as_df=True)
    print(user_role_df)

if __name__ == "__main__":
    main()