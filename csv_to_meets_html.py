import csv
import os

def get_gallery_images(folder_path):
    images = []
    # Loop through each folder in the gallery directory
    for folder in os.listdir(folder_path):
        folder_full_path = os.path.join(folder_path, folder)
        # Check if it is a directory
        if os.path.isdir(folder_full_path):
            # Add images in this directory
            for f in os.listdir(folder_full_path):
                if f.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    images.append(os.path.join(folder, f))  # Use the folder name
    return images

def csv_to_html(csv_filename, output_folder):
    # Derive the HTML filename by replacing the CSV extension with '.html' in the meets folder
    html_filename = os.path.join(output_folder, os.path.splitext(os.path.basename(csv_filename))[0] + '.html')

    with open(csv_filename, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

        # Ensure there are at least 5 rows for valid HTML generation
        if len(rows) < 5:
            print("CSV file must have at least 5 rows.")
            return

        # Extract values from the first five rows
        link_text = rows[0][0]
        h2_text = rows[1][0]
        link_url = rows[2][0]
        summary_text = rows[3][0]

        # Initialize HTML content
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{link_text}</title>
    <link rel="stylesheet" href="../css/reset.css">
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <a href="index.html" class="back-link">Back to Meets</a>
    <header class="sticky-header">
        <h1><a href="{link_url}">{link_text}</a></h1>
        <h2>{h2_text}</h2>
        <button id="toggle-dark-mode">Toggle Dark Mode</button>
    </header>
    <nav>
        <ul>
            <li><a href="#summary">Summary</a></li>
            <li><a href="#team-results">Team Results</a></li>
            <li><a href="#individual-results">Individual Results</a></li>
            <li><a href="#gallery">Gallery</a></li>
        </ul>
    </nav>
    <main id="main">
        <section class="summary" id="summary">
            <h2>Race Summary</h2>
            <div class="summary-content">
                <p id="summary-text">
                    {summary_text}
                </p>
            </div>
            <a href="#" id="read-more" onclick="toggleSummary()">Read more</a>
        </section>

        <!-- Start container for team results -->
        <section id="team-results">
            <h2>Team Results</h2>
            <div class="collapsible">
                <button class="collapsible-btn">Show Results</button>
                <div class="collapsible-content" style="display: none;">
                    <table>
                        <tr>
                        </tr>
"""

        # Loop through the remaining rows for team results
        for row in rows[4:]:
            # Check if the row has 3 columns (place, team, score)
            if len(row) == 3:
                html_content += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>\n"

        # Close the table and collapsible content
        html_content += """
                    </table>
                </div> <!-- collapsible-content -->
            </div> <!-- collapsible -->
        </section>
        
        <section id="individual-results">
            <h2>Individual Results</h2>
"""

        # Here, you need to loop through rows again for individual results
        for row in rows[4:]:
            if len(row) == 8 and row[5].strip().lower() == 'ann arbor skyline':  # Adjust as needed for your specific row structure
                place = row[0]
                grade = row[1]
                name = row[2]
                time = row[4]
                profile_pic = row[7]

                # Add the athlete div
                html_content += f"""
                <div class="athlete">
                    <figure>
                        <img src="../images/profiles/{profile_pic}" width="200" alt="Profile picture of {name}"> 
                        <figcaption>
                            <span class="athlete-name" onclick="toggleResults(this)">{name}</span>
                        </figcaption>
                    </figure>
                    <div class="results" style="display: none;">
                        <dl>
                            <dt>Place</dt><dd>{place}</dd>
                            <dt>Time</dt><dd>{time}</dd>
                            <dt>Grade</dt><dd>{grade}</dd>
                        </dl>
                    </div>
                </div>
"""

        # Get gallery images
        gallery_folder_path = os.path.join(output_folder, "gallery")
        images = get_gallery_images(gallery_folder_path)

        html_content += """<section id = "gallery">
        <h2>Gallery</h2>
        <div class="gallery-container">
"""
        # Loop through images and create image tags
        for image in images:
            # Construct the correct path based on the folder structure
            image_path = os.path.join("gallery", image)  # Use the image variable which includes the folder name
            html_content += f'<img src="{image_path}" alt="Gallery Image" class="gallery-image">\n'

        html_content += """
    </div> <!-- gallery-container -->
</section>

        
        </main>
        <footer>
            <p>
                Skyline High School<br>
                <address>
                    2552 North Maple Road<br>
                    Ann Arbor, MI 48103<br><br>
                </address>
                <a href="https://sites.google.com/aaps.k12.mi.us/skylinecrosscountry2021/home">XC Skyline Page</a><br>
                Follow us on Instagram <a href="https://www.instagram.com/a2skylinexc/" aria-label="Instagram"><i class="fa-brands fa-instagram"></i></a>
            </p>
        </footer>
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                const collapsibleButtons = document.querySelectorAll('.collapsible-btn');

                collapsibleButtons.forEach(button => {
                    button.addEventListener('click', function() {
                        this.classList.toggle("active");
                        const content = this.nextElementSibling;
                        if (content.style.display === "block") {
                            content.style.display = "none"; // Hide the results
                        } else {
                            content.style.display = "block"; // Show the results
                        }
                    });
                });
            });

            function toggleResults(element) {
                const resultsDiv = element.closest('.athlete').querySelector('.results');
                if (resultsDiv.style.display === 'block') {
                    resultsDiv.style.display = 'none'; // Hide the results
                } else {
                    resultsDiv.style.display = 'block'; // Show the results
                }
            }
        </script>

        <script>
            document.addEventListener('DOMContentLoaded', () => {
                // Check for saved user preference
                if (localStorage.getItem('dark-mode') === 'enabled') {
                    document.body.classList.add('dark-mode');
                }

                document.getElementById('toggle-dark-mode').addEventListener('click', function() {
                    document.body.classList.toggle('dark-mode');
                    // Save user preference
                    if (document.body.classList.contains('dark-mode')) {
                        localStorage.setItem('dark-mode', 'enabled');
                    } else {
                        localStorage.setItem('dark-mode', 'disabled');
                    }
                });
            });
        </script>
        <script>
        function toggleSummary() {
            const summaryContent = document.querySelector('.summary-content');
            const readMoreLink = document.getElementById('read-more');
            
            // Toggle expanded class
            summaryContent.classList.toggle('expanded');

            // Change link text based on state
            if (summaryContent.classList.contains('expanded')) {
                readMoreLink.textContent = 'Read less'; // Change text when expanded
            } else {
                readMoreLink.textContent = 'Read more'; // Change text when collapsed
            }
        }
        </script>
</body>
</html>
"""
        
        # Save HTML content to a file in the meets folder
        with open(html_filename, 'w', encoding='utf-8') as htmlfile:
            htmlfile.write(html_content)

        print(f"HTML file '{html_filename}' created successfully.")

def process_meet_files():
    # Set the meets folder path
    meets_folder = os.path.join(os.getcwd(), "meets")
    
    # Search for all CSV files in the meets folder
    csv_files = [f for f in os.listdir(meets_folder) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"No CSV files found in folder: {meets_folder}")
        return

   
