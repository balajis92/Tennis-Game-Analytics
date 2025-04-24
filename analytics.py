import mysql.connector
import streamlit as st
import pandas as pd
import time
import seaborn as sns

# Database connection
def connect_to_db():
    return mysql.connector.connect(
        host='localhost', user='root', password='bala123', database='sportradar'
    )

st.set_page_config(page_title="Tennis Rankings", layout="wide")

# Navigation
menu = st.sidebar.radio(
    "Navigate",
    ("Home", "Competitor Details", "Rank Range", "Country Filter", 
     "Competition Type", "Category", "Venues by Country", "Leadership Board")
)

# Helper functions
def fetch_query_results(query, params=None):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_df_from_query(query, columns, params=None):
    results = fetch_query_results(query, params)
    return pd.DataFrame(results, columns=columns)

# Page content
if menu == "Home":
    st.title('Tennis Rankings :tennis:')
    st.divider()
    st.write("""**Tennis** is a popular sport played between two individuals (singles) or two teams of two players each (doubles),
 where the objective is to hit a ball over a net into the opponent's side of the court in such a way that they cannot return it within the rules of the game.""")
    st.subheader("Types of Tennis")
    st.write("**Singles**: One-on-one match between two players.")
    st.write("**Doubles**: A match between two teams of two players each, requiring more coordination and teamwork.")

elif menu == "Competitor Details":
    st.title("Competitor Details")
    st.divider()
    st.write("**Select a competitor from the sidebar to view their details.**")
    
    # Get competitor names
    options = [row[0] for row in fetch_query_results("SELECT name FROM competitors ORDER BY name ASC")]
    selected_option = st.sidebar.selectbox("Select Competitor Name", options)
    
    if selected_option:
        st.write(f"**Details of competitor**: {selected_option}")
        data = get_df_from_query(
            "SELECT co.name, cr.rank, cr.movement, cr.points, cr.competitions_played, co.country FROM competitors co JOIN competitor_rankings cr ON cr.competitor_id=co.competitor_id WHERE name = %s",
            ['name', 'rank', 'movement', 'points', 'competitions_played', 'country'],
            (selected_option,)
        )
        st.write(data)

elif menu == "Rank Range":
    st.title("Competitor Rank Range")
    st.divider()
    
    with st.spinner("Loading data..."):
        time.sleep(1)
    
    rank_range = st.sidebar.slider("Rank Range", min_value=1, max_value=500, value=(1, 500), step=1)
    
    if rank_range:
        st.write(f"**Details of rank range**: {rank_range}")
        rank_data = get_df_from_query(
            "SELECT cr.rank, co.name, cr.movement, cr.points, cr.competitions_played, co.country FROM competitor_rankings cr JOIN competitors co ON cr.competitor_id=co.competitor_id WHERE `rank` BETWEEN %s AND %s ORDER BY `rank`",
            ['rank', 'name', 'movement', 'points', 'competitions_played', 'country'],
            (rank_range[0], rank_range[1])
        )
        st.write(rank_data)
        
        # Scatter plot
        plot = sns.relplot(x='rank', y='competitions_played', data=rank_data, kind="scatter")
        st.pyplot(plot.fig)

elif menu == "Country Filter":
    st.title("Country Filter")
    st.divider()
    
    # Get countries
    country_options = [row[0] for row in fetch_query_results("SELECT DISTINCT country FROM competitors ORDER BY country ASC")]
    selected_country = st.sidebar.selectbox("Select Country", ["All"] + country_options)
    
    if selected_country:
        st.write(f"**Details for Country:** {selected_country}")
        
        # Country statistics
        country_data = get_df_from_query(
            """SELECT COUNT(co.competitor_id) AS Total_no_of_competitors,
               AVG(cr.points) AS Average_points, co.country 
               FROM competitor_rankings cr 
               JOIN competitors co ON cr.competitor_id = co.competitor_id
               WHERE co.country = %s
               GROUP BY co.country""",
            ['Total Competitors', 'Average Points', 'Country'],
            (selected_country,)
        )
        
        if not country_data.empty:
            st.dataframe(country_data)
            
            # Individual players
            details_df = get_df_from_query(
                """SELECT co.name, cr.points, co.country 
                FROM competitor_rankings cr 
                JOIN competitors co ON cr.competitor_id = co.competitor_id 
                WHERE co.country = %s""",
                ['Name', 'Points', 'Country'],
                (selected_country,)
            )
            
            if not details_df.empty:
                st.subheader("Competitor Details")
                st.dataframe(details_df)
            else:
                st.warning("No competitors found for the selected country.")
        else:
            st.warning("No data available for the selected country.")

elif menu == "Competition Type":
    st.header("Competition Type")
    st.divider()
    
    with st.spinner("Loading data..."):
        time.sleep(1)
    
    competition_type = st.sidebar.radio("Competition Type", ['Singles', 'Doubles', 'mixed'])
    
    if competition_type:
        st.write(f"**Competition Type**: {competition_type}")
        type_data = get_df_from_query(
            "SELECT competition_id, competition_name, type FROM competitions WHERE type = %s LIMIT 200",
            ['competition_id', 'competition_name', 'type'],
            (competition_type,)
        )
        st.write(type_data)

elif menu == "Category":
    st.header("Category")
    st.divider()
    
    # Get categories
    category_options = [row[0] for row in fetch_query_results("SELECT category_name as category FROM categories")]
    category_option = st.sidebar.selectbox("Select Category", category_options)
    
    if category_option:
        st.write(f"**Details of category**: {category_option}")
        category_data = get_df_from_query(
            "SELECT co.competition_name as competition FROM competitions co JOIN categories ca ON co.category_id=ca.category_id WHERE category_name= %s",
            ['competition'],
            (category_option,)
        )
        st.write(category_data)

elif menu == "Venues by Country":
    st.header("Venues by Country")
    st.divider()
    
    with st.spinner("Loading data..."):
        time.sleep(1)
    
    # Get venue countries
    venue_country_options = [row[0] for row in fetch_query_results("SELECT DISTINCT country_name FROM venues")]
    venue_option = st.sidebar.selectbox("Venues by country", venue_country_options)
    
    if venue_option:
        st.write(f"**Details of venues**: {venue_option}")
        venue_data = get_df_from_query(
            "SELECT v.venue_id, v.venue_name, c.complex_name, v.city_name FROM venues v JOIN complexes c ON v.complex_id=c.complex_id WHERE country_name= %s LIMIT 500",
            ['venue_id', 'venue_name', 'complex', 'city'],
            (venue_option,)
        )
        st.write(venue_data)

elif menu == "Leadership Board":
    st.header("Leadership Board")
    st.divider()
    
    leader_data = get_df_from_query(
        "SELECT cr.rank, c.name, cr.points FROM competitor_rankings cr JOIN competitors c ON cr.competitor_id=c.competitor_id WHERE cr.rank <= 5 ORDER BY cr.rank ASC, cr.points DESC",
        ['Rank', 'Name', 'Points']
    )
    
    st.write("**Top 5 Rank:**")
    st.write(leader_data)
    st.area_chart(leader_data, x='Rank', y='Points')