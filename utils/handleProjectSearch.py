'''handle project search'''
from models.project import Project
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