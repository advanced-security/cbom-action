### PQC Action

#### Workflows

1. Customer CBOM repo runs Actions workflow
   - Create/update dependency graph
   - For each dependency look up CBOM info from centralised database
   - For each dependency that does not have CBOM info pull from GraphQL API to locate dependency repo information
   - Either
     - Attempt to checkout and run PQC query analysis
     - Post repo information centrally to queue a PQC query analysis (perhaps using GH Actions minutes rather than customer)
   - Output CBOM info

2. Scheduled Actions worklflow in GH repo
   - Pull list of top 100 dependencies for in scope package ecosystems
   - Pull list of dependencies previously analysed but no longer in top 100
   - Merge lists
   - For each dependency
     - Pull repo information
     - Pull version list since last workflow run
     - For each new version
       - Queue PQC query analysis
       - Store results of analysis centrally
      
#### Questions

1. How do we manage the situation where a customer repo workflow has many dependencies that have not yet been analysed? Attempting to analyse in the workflow could take a long time, consume considerable Actions minutes on the customer account, and result in large numbers of failures where CodeQL Autobuild does not work.
2. What data structure and storage format makes sense for the central store of dependency CBOM data? A repo with a `ecosystem -> namespace -> package -> version` folder structure may work if each CBOM output file is stored for each version (e.g. the CycloneDX output file). Private vulnerabilities have been discussed as an option but I (@ctcampbell) don't love identifying something as a vulnerability when it isn't actually one yet.
