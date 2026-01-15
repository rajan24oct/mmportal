Tasks:
1. Invitation
	- [x] Invite user from backend for mentor/user
	- [x] User accept invitation and profile will be created
	- [x] User will be redirected to profile page
2. User
    - [x] Search mentor
        - [x] Add is_mentor field to UserProfile if not exists
        - [x] Create a search view for mentors
        - [x] Create a template for mentor search results
    - [x] Ask for connect
        - [x] Create ConnectionRequest model
        - [x] Create view to send connection requests
        - [x] Create view to list/accept/reject connection requests
	- [x] Create message functionality between two users
	- [x] CheckUser Profile /my-profile-about/
		- [x] Create a about field in UserProfile
			- [x] On profile edit, it will be updated
			- [x] Fetch about from backend in overview section
		- [x] Fetch connection from backend in connection section
			- [x] Connection should message each other
			- [ ] Connection should be removed as per given button
			- [ ] Implement functionality for "Load more Connection"
		- [ ] Fetch post from backend in post section of respective user profile
		- [ ] Fetch media from backend in media section of respective user profile

3. Group 
    - [x] Create group skeleton 
        - [x] Create Group model 
        - [x] Create GroupMembership model
    - [x] Create group from backend
    - [x] Assign moderator to group
    - [x] User can find group
    - [x] Send invitation to join group
    - [x] Moderator can approve user
    - [x] User can chat with group
    - [x] User can like, unlike, comment, chat
    - [x] User can upload image, video


