'''handle project update and create'''

from models.link import Link
from models.objective import Objective
from models.takeaway import Takeaway
from models.subtitle import Subtitle

def update_links(links_data, project):
    """Update project links"""
    # Delete existing links
    for link in project.links:
        link.delete()

    # Create new links from the form data
    for link_data in links_data:
        if link_data['name']:  # Check if 'name' field is not empty
            link = Link(name=link_data['name'], url=link_data['url'], project_id=project.id)
            link.save()


def update_subtitles(subtitles_data, project):
    """Update project subtitles and objectives"""
    # Delete existing objectives
    for subtitle in project.subtitles:
        subtitle.delete()

    # Create new objectives from the form data
    for subtitle_data in subtitles_data:
        if subtitle_data['text']:
            subtitle = Subtitle(text=subtitle_data['text'], project_id=project.id)
            subtitle.save()
        for objective_data in subtitle_data['objectives']:
            if objective_data['text']:  # Check if 'text' field is not empty
                objective = Objective(text=objective_data['text'], project_id=project.id, subtitle_id=subtitle.id)
                objective.save()


def update_takeaways(takeaways_data, project):
    """Update project takeaways"""
    # Delete existing takeaways
    for takeaway in project.takeaways:
        takeaway.delete()

    # Create new takeaways from the form data
    for takeaway_data in takeaways_data:
        if takeaway_data['text']:  # Check if 'text' field is not empty
            takeaway = Takeaway(text=takeaway_data['text'], project_id=project.id)
            takeaway.save()

def create_links(links_data, project):
    """create project links"""
    for link_data in links_data:
        if link_data['name']:  # Check if 'name' field is not empty
            link = Link(name=link_data['name'], url=link_data['url'], project_id=project.id)
            link.save()


def create_subtitle(subtitles_data, project):
    """create project subtitles and objectives"""
    for subtitle_data in subtitles_data:
        if subtitle_data['text']:
            subtitle = Subtitle(text=subtitle_data['text'], project_id=project.id)
            subtitle.save()
        for objective_data in subtitle_data['objectives']:
            if objective_data['text']:  # Check if 'text' field is not empty
                objective = Objective(text=objective_data['text'], project_id=project.id, subtitle_id=subtitle.id)
                objective.save()


def create_takeaways(takeaways_data, project):
    """create project takeaways"""
    for takeaway_data in takeaways_data:
        if takeaway_data['text']:  # Check if 'text' field is not empty
            takeaway = Takeaway(text=takeaway_data['text'], project_id=project.id)
            takeaway.save()