import streamlit as st
import pandas as pd
import time
from datetime import datetime
import sys
import traceback

# Configure Streamlit page
st.set_page_config(
    page_title="Youtube Scraper App",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🛒 Youtube Data Scraper")
    st.markdown("---")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Search parameters
        search_query = st.text_input(
            "Search Query", 
            placeholder="e.g., wireless headphones",
            help="Enter the product you want to search for"
        )
        
        max_results = st.slider(
            "Max Pages to Scrape", 
            min_value=10, 
            max_value=50, 
            value=5,
            help="Number of pages to scrape (more pages = more results but slower)"
        )
        scrolls = st.slider(
            "Scrolls per Page", 
            min_value=1, 
            max_value=10, 
            value=3,
            help="Number of scroll actions to load more results")
        
        delay_between_requests = st.slider(
            "Delay Between Requests (seconds)", 
            min_value=1, 
            max_value=10, 
            value=3,
            help="Delay to avoid being blocked by Amazon"
        )
        
        st.markdown("---")
        st.markdown("### 📝 Instructions")
        st.markdown("""
        1. Enter your search query
        2. Configure scraping parameters
        3. Click 'Start Scraping'
        4. Wait for results to load
        5. Download the results as CSV
        """)
        
        st.markdown("---")
        st.markdown("### 🛠️ Debug Mode")
        debug_mode = st.checkbox("Enable Debug Mode")
        if debug_mode:
            st.warning("debug mode on")
            try:
        
          
                if st.button("Test Scraper Import"):
               
                
                
                
                      
                  from youtube_scraper import web_scraper
                    
                  st.success("✅ Scraper imported successfully!")
                #   st.info(f"Scraper type: {type(scraper)}")
            
            # if st.error("scraper module not found")
          
            except Exception as e:
                st.error(f"❌ Import failed: {e}")
                st.code(traceback.format_exc())
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Search Configuration")
        
        # Display current settings
        if search_query:
            st.info(f"**Query:** {search_query} | **Pages:** {max_results} | **Delay:** {delay_between_requests}s")
        else:
            st.warning("Please enter a search query in the sidebar")
    
    with col2:
        start_scraping = st.button(
            "🚀 Start Scraping", 
            type="primary",
            disabled=not search_query,
            use_container_width=True
        )
    
    # Results section
    if start_scraping and search_query:
        st.markdown("---")
        st.subheader("🔄 Scraping in Progress...")
        
        # Progress indicators
        progress_bar = st.progress(10)
        status_text = st.empty()
        results_container = st.container()
        
        try:
            # Import and initialize scraper
            status_text.text("Importing scraper modules...")
            progress_bar.progress(10)
            
            try:
                from youtube_scraper import web_scraper
                status_text.text("✅ Successfully imported scraper modules")
                progress_bar.progress(20)
                
            except ImportError as e:
                st.error(f"❌ Error importing scraper modules: {e}")
                st.markdown("""
                **Possible solutions:**
                1. Make sure `webs1.py` is in the same directory
                2. Install required dependencies: `pip install requests beautifulsoup4 pandas`
                3. Check if the module name is correct
                """)
                return
            
            # Start scraping
            status_text.text(f"🔍 Searching for: {search_query}")
            progress_bar.progress(30)
            
            # Initialize scraper and get results
            try:
                all_results = web_scraper(search_query, max_results, scrolls)
                status_text.text(f"📄 Scraping {max_results} page(s)...")
                progress_bar.progress(50)
                
                # Add delay before scraping
                time.sleep(delay_between_requests)
                
                # Call your scraper
                
                
                progress_bar.progress(90)
                status_text.text("📊 Processing results...")
                
                
                    # Convert to DataFrame
                df = all_results
                    
                progress_bar.progress(100)
                status_text.text(f"✅ Scraping completed! Found {len(all_results)} products")
                    
                    # Display results
                with results_container:
                        st.subheader(f"📋 Results ({len(all_results)} products found)")
                        
                        # Metrics
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Products", len(all_results))
                        with col2:
                            if 'price' in df.columns:
                                # Handle price column more carefully
                                try:
                                    prices = pd.to_numeric(df['price'].astype(str).str.replace(r'[$,₹]', '', regex=True), errors='coerce')
                                    avg_price = prices.mean() if not prices.empty and not prices.isna().all() else 0
                                    st.metric("Avg Price", f"${avg_price:.2f}")
                                except:
                                    st.metric("Avg Price", "N/A")
                        with col3:
                            if 'rating' in df.columns:
                                try:
                                    ratings = pd.to_numeric(df['rating'], errors='coerce')
                                    avg_rating = ratings.mean() if not ratings.empty and not ratings.isna().all() else 0
                                    st.metric("Avg Rating", f"{avg_rating:.1f}⭐")
                                except:
                                    st.metric("Avg Rating", "N/A")
                        with col4:
                            st.metric("Pages Scraped", max_results)
                        
                        # Data table
                        st.dataframe(
                            df, 
                            use_container_width=True,
                            height=400
                        )
                        
                        # Download button
                        csv = df.to_csv(index=False)
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"amazon_scrape_{search_query.replace(' ', '_')}_{timestamp}.csv"
                        
                        st.download_button(
                            label="📥 Download Results as CSV",
                            data=csv,
                            file_name=filename,
                            mime="text/csv",
                            use_container_width=True
                        )
                
                # else:
                #     progress_bar.progress(100)
                #     status_text.text("❌ No results found")
                #     st.warning("No products were found. This could be due to:")
                #     st.markdown("""
                #     - **Network issues** or Amazon blocking requests
                #     - **Invalid search query** - try a more common product name
                #     - **Scraper detection** - try increasing the delay between requests
                #     - **Changes in Amazon's page structure** - the scraper might need updates
                #     """)
                    
            except Exception as scraper_error:
                st.error(f"⚠️ Error during scraping: {scraper_error}")
                st.markdown("**Troubleshooting tips:**")
                st.markdown("""
                1. Check your internet connection
                2. Try a different search query
                3. Increase the delay between requests
                4. Make sure your scraper handles Amazon's anti-bot measures
                """)
                st.code(traceback.format_exc())
                
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {e}")
            st.code(traceback.format_exc())
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>⚠️ Please respect Amazon's robots.txt and terms of service when scraping</p>
        <p>Use responsibly with appropriate delays between requests</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()


