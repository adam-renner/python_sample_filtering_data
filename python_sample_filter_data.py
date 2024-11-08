def filter_data(input_file, output_file, keywords_file):
  """
  Project:        Identifying nonprofits within certain categories using publically available IRS tax data
  Description of script: 
                  This script uses a list of keywords in a separate file to reduce the size of the dataset and remove data that
                  is not relevant. The dataset only had limited information and, while the IRS had a search tool, it could only
                  look for one term per search. If a keyword is identified in a line from the input file, it is saved into the 
                  output file.
  Notes:          "Publication 78" data downloaded from https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads#pub78
  Author:         Adam Renner
  Date Created:   06/20/2024
  Last Revision:  07/23/2024
  
  Args:
      input_file (str): File path to the input text file. Must be in PSV format.
      output_file (str): File path to the output text file. Will output in PSV format.
      keywords_file (str): Path to the text file containing keywords (one per line).
  """
  with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    # Skip header line
    next(infile)
    # Read keywords from the file and create a list
    keywords = []
    with open(keywords_file, 'r') as keyword_file:
      for line in keyword_file:
        keyword = line.strip().lower()  # Remove whitespace and convert to lowercase
        if keyword:  # Skip empty lines
          keywords.append(keyword)
    
    state_list = []
    state_list = list(selected_states.lower().split(',')) # Converting selected states into lowercase list

    # Skip any empty lines
    for line in infile:
      if line.strip() == "":
        continue
      data = line.strip().split('|') # input file is in psv format
      name = data[1].lower()  # Convert name to lowercase for case-insensitive matching
      org_state = data[3].lower() # States should be all upper-case, but converting to ensure consistancy
      
      if any(keyword in name for keyword in keywords): # Check if any keyword appears in the name (case-insensitive)
        if any(state in org_state for state in state_list):  # Check if organization is in selected states (case-insensitive)
          outfile.write("|".join(data) + "\n") # writing back into psv format and moving to next line

# Replace with appropriate file paths and state(s)
input_file = "p78_samp.txt"
output_file = "filtered_samp.txt"
keywords_file = "keyword_samp.txt"
selected_states = "VA,DC,MD"

filter_data(input_file, output_file, keywords_file)

print("Data filtered and saved to", output_file)
