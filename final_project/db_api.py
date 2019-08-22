from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ENGINE = create_engine('sqlite:///./data.db',
                       connect_args={'check_same_thread': False})
Session = sessionmaker(bind=ENGINE)


def create_link_record(user_id, long_link, short_link, created_at):
    s = Session()
    s.execute("INSERT INTO links (user_id, long_link, short_link, created_at) VALUES ({}, \"{}\", \"{}\", {})".format(
        user_id, long_link, short_link, created_at)
    )
    s.commit()


def get_links(limit=10, offset=0):
    s = Session()
    rows = s.execute("SELECT clicks, short_link FROM links LIMIT {} OFFSET {}".format(
        limit, offset
    )).fetchall()

    return rows


def update_link_clicks(short_link, clicks):
    s = Session()
    s.execute("UPDATE links SET clicks={} WHERE short_link=\"{}\"".format(
        clicks, short_link
    ))
    s.commit()


def get_top_links(user_id, created_after=0, limit=10):
    s = Session()
    rows = s.execute("SELECT short_link, clicks FROM links WHERE user_id = {} AND created_at > {} "
                     "ORDER BY clicks DESC LIMIT {}".format(
        user_id, created_after, limit
    )).fetchall()

    return rows
