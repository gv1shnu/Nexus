# Search Nexus

Search Nexus is a flask-based application that allows users to perform searches across multiple search engines simultaneously and view the results in one place.

## Features

- Perform searches across multiple search engines simultaneously.
- View search results from various search engines in one consolidated view.
- Experimental in nature.

## Usage

- Download SearchNexus application directly from [here](https://drive.google.com/file/d/1fmbicfMMcl1JeaqiIOYOltmZAEz-CWah/view?usp=sharing).
- Enter your search query in the search box on the home page.
- Press Enter to initiate the search.
- Search results from multiple search engines will be displayed within seconds.

**Note**: Make sure Chrome is your default browser. It helps. 

## Demo

Please view following demo in different formats.


### Video
  Click [here](https://youtu.be/yyqwyAamiaQ) to watch the **latest** demo on YouTube.

### Homepage screenshot

  Look at the following screenshots for old demo.


![Screenshot (1)](https://github.com/gv1shnu/SearchNexus/assets/121789146/98b0fee5-2b3f-4e04-b81f-2b9d08c4e101)

## Installation

Follow these steps to set up and run the Search Nexus Flask application:

1. Clone the repository:
	
   		git clone https://github.com/gv1shnu/SearchNexus.git


2. Navigate to the project directory:
	
   		cd SearchNexus


3. To run this project, make sure you have Python 3.11 and pip installed on your system. Install the required dependencies:
	
		pip install -r requirements.txt


4. Start the Flask development server:

		python app.py

## Technologies Used

- Flask: A micro web framework for Python programming language.
- HTML5: The markup language used for structuring the web pages.
- CSS3: The stylesheet language used for styling the web pages.

## Limitations

- The search results may not always be consistent across different search engines due to variations in algorithms and indexing.
- The application relies on the availability and performance of the search engines it queries.
- The application currently supports a predefined set of search engines and cannot dynamically add or remove search engines.

## Contributing

Contributions and code reviews are welcome! 

TODO
----
- [ ] Update the blurry icon
- [ ] Order rank-wise
- [x] Center the result-container div
- [x] Properly scrape for YouTube video description again
- [ ] Add more search engines
- [ ] Pagination
- [ ] Change the background of success.html
- [x] Organize displayed search results more comprehensively (card style)

## License

This project is licensed under the [MIT License](LICENSE).
