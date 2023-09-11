# Second Brain Synapse

## SetUp

* Create `/config.ini` following `config.ini.template` as example.

## Installation

* #TBD

## Execution

* `python -m src`

## Product Specs

1. Create `Projects Index`.
   1. Iterate over every project folder in `/02_projects`.
   2. Extract the project's name from folder name into `project_name: str`, making sure:
      1. Project name is lower cased.
      2. White spaces in project name are replaced by underscore.
      3. Project name is url safe.
   3. Read in all `.md` files, excluding content within code blocks, e.g. ```abc```.
   4. Concatenate all non-excluded content into a single temp text file.
   5. Pass temp text file content to LLM (GPT4).
      1. Generate summary description of the project.
      2. Generate list of main topics, concepts, named entities, and events contained in the project material.
      3. Generate content index.
      4. Infer state of project. -> Requires [Auditing Projects](#auditing-projects) component.
   6. If `f"/02_projects/<project_name>/00_<project_name>_meta.md"` doesn't exist already, create it.
   7. Append LLM-generated content into created `.md` file.
   8. Concatenate into a `semantic_summary`:
      1. Project name.
      2. LLM-generated project summary description
      3. LLM-generated project list of main topics, concepts, named entities, and events.
   9. Create project entry `{<project_name>: <semantic_summary>}: dict`.
   10. Update project entry in `04_memory/project_memory.json` by:
       1. Update `<semantic_summary>` data for key `<project_name>` for an existing project.
       2. Create new key `<project_name>` and insert `<semantic_summary>` data for non-existant project (i.e. the `<project_name>` key does not exist in the index).
2. Create `References Index`
   1. #TODO: (Relatively similar process as for `Projects Index`)
3. Process captured items
   1. Iterate over every `.md` file in folder `/00_capture`.
   2. Read in `.md` file excluding content within code blocks, e.g. ```abc```.
   3. Pass content to LLM.
      1. Create short summary description of the captured item.
      2. Classify if the captured item corresponds to an `action` or a `reference`.
      3. Infer related project/s. -> [Project Memory](#project-memory)
      4. Infer association to existing reference material. -> [Reference Memory](#reference-memory)
      5. Identify tagged action items (i.e. TODO).
         * For every action item:
            1. Generate short 3-5 word title (to use as future filename).
            2. Generate detailed action item description.
      6. Generate `## Item Metadata` section below the item title (i.e. below H1):
         * `Description`: ...
         * `Item Type`: [action, reference]
         * `Action Items`: [action_1, action_2, ...]
         * `Associated Projects`: [project_1, project_2, ...]
         * `Associated References`: [reference_1, reference_2, ...]
   4. For every action item in `Action Items`:
      1. Create an individual `.md` file for it.
      2. #TODO

### Processing Captured Items

* #TODO

### Processing Actionable Items

* Heuristics:
  1. Read only `.md` files.
  2. Skip content within code blocks, e.g. ```abc```.

* Process:
  1. Ignore `03_reference`

### Auditing Projects

* #TODO

### Leveraging Reference Material

* #TODO

#### Retrieving Relevant Reference Material

* #TODO

#### Correlating Reference Material

* #TODO

### Memory

#### Ontological Memory

* #TODO

#### Actions Memory

* #TODO

#### Project Memory

* #TODO

#### Reference Memory

* #TODO

## Work Breakdown Structure

### Now

* Create `config.ini` file for project configuration variables, such as second brain's filepath in local system. #DONE
* Create `config.ini.template` for sharing, while keeping `config.ini` ignored in `.gitignore`. #DONE
* Add MIT license. #DONE
* Create `pyproject.toml` for setting up basic packaging. #DONE
