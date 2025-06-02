# Group project in AI2 Data Engineering
## How to run the program
| Steps | Command |
| --- | --- |
| Clone the repo | `git clone https://github.com/aeriesAce/AI2_group_project.git` |
| Navigate to the project root | `cd AI2_group_project` |
| Create a virtual enviroment | `uv venv .venv` |
| Activate the enviroment for Windows in PS | `.venv\Scripts\activate` |
| Activate the enviroment for Mac/Linux | `source source .venv/bin/activate` |
| Install the dependencies | `uv pip install -r requirements.lock.txt` |

### First time run
| Steps | Command |
| --- | --- |
| Navigate to the dbt project folder | `cd dbt_groupp` |
| Install dbt dependencies | `dbt deps` |
| Navigate back to the root folder | `cd ..` |
| Run the data pipeline | `python Data/pipeline.py` |
| Launch the dashboard | `streamlit run main.py` |

### To use Gemeni
| Steps | Command |
| --- | --- |
| Get an API key | [Here](https://ai.google.dev/gemini-api/docs/api-key) |
| Log in with your Google account |  |
| Create a .env file in local repo and put api key in the .env file | `API_KEY = "KEY HERE` |

## Scenario
<details open>
<summary>Click to hide/show</summary>
You are a data engineer for a HR agency. 
Here's an overview of the business model of this agency:

Talent acquisition specialists work with different occupation fields. According to the opening job ads on
**Arbetsförmedlingen**, they will:
- Search and contact potential candidates from LinkedIn.
- Contact and market those potential candidates to corresponding employers.

Therefore, they constantly analyze job ads in order to understand which types of candidates they should
approach.

### Challenges
Currently, every beginning of the week, they manually browse the homepage of **Arbetsförmedlingen** and download a list of opening job ads to guide their work over the week. 
However,
they are not able to draw insights from these job ads as:
- The information are messy
- They have spent too much time to manually collect and clean data so that they do not have much time
to analyze the data, which is important to improve the efficiency of their work
</details>

### Test & documentation
<details>
<summary>Click to show/hide</summary>

### Implemented tests

#### Schema tests
- `not_null` on all dimensional tables
- `relationships`:
  - All foreign keys in `fct_job_ads` to reference their respective dimension table

#### Manual testing
- Additional data checks (nulls, value distributions, integrity) were manually tested and explored using `duckdb-ui`

### Documentation
- All models documented with `description` in `schema.yml`
- Column-level documentation in `fct_job_ads`
- Flow and Lineage docs:
[Flowchart](Lineage_Flowchart/flow_diagram.drawio.png)
[Lineage](Lineage_Flowchart/dbt-dag.png)
</details>

## The team:
Rickard
Max
Salih
Elvira
