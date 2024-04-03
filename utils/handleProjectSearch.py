'''handle project search'''
from models.project import Project
from models.user import Profile
from models import storage


def project_search(searchQuery):
    '''search project by title, tags,
       objectives, takeaways, description
    '''
    projects = []
    searchQuery = searchQuery.lower()
    for project in storage.all(Project).values():
        if searchQuery in project.title.lower() or\
              (project.description and searchQuery in\
               project.description.lower()):
                projects.append(project)
        else:
            for tag in project.tags:
                if searchQuery in tag.name.lower():
                    projects.append(project)
                    break
            if project not in projects:
                for objective in project.objectives:
                    if searchQuery in objective.text.lower():
                        projects.append(project)
                        break
            if project not in projects:
                for takeaway in project.takeaways:
                    if searchQuery in takeaway.text.lower():
                        projects.append(project)
                        break
            if project not in projects:
                for link in project.links:
                    if searchQuery in link.name.lower():
                        projects.append(project)
                        break
    return projects


def profile_search(searchQuery):
    '''profiles search'''
    profiles = []
    for profile in storage.all(Profile).values():
                if (profile.name and searchQuery in profile.name.lower()) or (profile.bio and searchQuery in profile.bio.lower()):
                        profiles.append(profile)
                else:
                    for skill in profile.skills:
                        if searchQuery in skill.name.lower():
                            profiles.append(profile)
                            break
    return profiles