import pcycopg2

conn=psycopg2.connect(
    host="localhost", 
    database="home_work11",
    user="postgres",
    password="a1100130a"

)

cur = conn.cursor()


cur.execute ("""
# ------------------------------------ 1 start create table-----------------------------------------------------------------
drop table if exists  commentss;
drop table if exists news;
drop table if exists categories;

create table if not exists categories (
	id serial primary key,
	categoriy_name varchar(100) not null,
	description text not null
);
-- 2
create table if not exists news(
	id serial primary key,
	category_id int ,
	title varchar(200) not null,
	contents  text not null,
	published_at timestamp default current_timestamp,
	is_published bool,
	foreign key (category_id) references categories(id)
);
-- 3
create table if not exists commentss(
	id serial primary key,
	news_id	int ,
	author_name	varchar(100),
	comment_text text not null,
	creared_at	timestamp default current_timestamp,
	foreign key	(news_id) references news(id)
);

# -------------------------- the end create--------------------------------------------------

); 
""")
cur.execute("""
# --------------------------------------2 start alter table--------------------------------------------------------------------------
-- 1
alter table news	
add	column  views int	 default o;
-- 2
alter table commentss
alter column author_name set data type   text;


# ---------------------------the end alter table------------------------------------------------------------

""")

cur.execute("""

# ---------------------------	3 start insert into------------------------------------------------

insert into categories (categoriy_name, description) 
values
('Technology', 'Latest technology news and articles.'),
('Sports', 'All about sports, teams, and events.'),
('Health', 'Health tips, wellness, and medical news.'),
('Entertainment', 'Movies, TV shows, music, and celebrity news.'),
('Business', 'Business trends, finance, and economy news.');


insert into news (category_id, title, contents, is_published) 
values
(1, 'New AI Technology Breakthrough', 'Researchers have developed a new AI technology that promises to revolutionize the industry.', TRUE),
(2, 'Football World Cup 2024: Teams and Predictions', 'The 2024 FIFA World Cup is approaching, and teams are already preparing for the big event.', TRUE),
(3, 'New Health Study Reveals Benefits of Meditation', 'A new study shows how meditation can significantly improve mental health and reduce stress levels.', TRUE),
(4, 'Top 10 Movies of the Year', 'Discover the best movies released this year that are receiving great reviews from critics and audiences alike.', TRUE),
(5, 'Stock Market Analysis: What’s Next?', 'Experts share their predictions for the stock market and economy in the coming months.', TRUE);


insert into commentss (news_id, author_name, comment_text) 
values
(1, 'John Doe', 'This AI technology is going to change everything! Can’t wait to see how it develops.'),
(2, 'Jane Smith', 'I think Brazil will win this year’s World Cup. They have a great team!'),
(3, 'Alice Johnson', 'Meditation has really helped me reduce stress. I’m glad to see more studies supporting it.'),
(4, 'Bob Lee', 'I loved the movie reviews! Definitely going to watch some of these.'),
(5, 'Carlos Mendez', 'I’m optimistic about the stock market. There are some great opportunities coming up.');

# --------------------------------------the end insert-------------------------------------------------------------------


""")

cur.execute("""
# --------------------------------------4 start upadate-------------------------------------------------------------------

# 1
update news
set views =views+1;
# 2
update news
set is_published= true	where published_at<= current_timestamp -  interval '1 day'
and (is_published is null or is_published = false)

# ------------------------------------ the end update---------------------------------------------------------------------

""")
cur.execute("""
# ------------------------------------	5 start delete--------------------------------------------------
delete from news
where published_at <= current_timestamp -  interval '1 year'

# -----------------------------------------the end delete-------------------------------------------------------------

""")

cur.execute("""
# ------------------------------------------ 6 start select------------------------------------------------------
-- 1
select news.id,   news.title,   categories.categoriy_name 
from news  join  categories  on news.category_id = categories.id

-- 2
select news.id,  news.title , categories.categoriy_name
from news join categories
on news.category_id = categories.id
where categories.categoriy_name='Technology';

-- 3
select news.id , news.title , news.published_at
from news	where news.is_published = true
order by news.published_at	desc
limit 5 ;

-- 4
select news.id, news.title , news.views
from news	where news.views between 10 and 100;

-- 5
select commentss.author_name
from commentss
where commentss.author_name like ('A%');

-- 6
select commentss.id, commentss.comment_text, commentss.author_name
from commentss
where commentss.author_name is null ;

-- 7
select count(description) as count_cat from categories

# -- agar tepadagini ^  hato tushungan bolsam 
# --bunisi tori  db oyleman ==> 

select categories.categoriy_name, count(news.id) 
from categories  left join news  on news.category_id = categories.id
group by categories.categoriy_name;
# ----------------------------the end select------------------------------------------------------
""")
cur.execute("""
# ----------------------------7 start limit add----------------------------------------------------------

alter table news
add constraint	unique_tit unique (title);
# -----------------------the end project--------------------------------------------------------------------
""")


cur.close()
conn.close()
