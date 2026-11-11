# G15 / P21 – M4 Design Decision and Testing

## Current Status

We have completed the M4 code and tested it locally. All three tests passed. We still need to upload the changes to GitHub, get the group to review them, update our shared workbook and create the `PRE_EVENT_B` tag.

## 1. Background and Problem Identified

During M2, we tested Code2DFD's results across four microservice applications and achieved an overall F1 score of 0.855.

For Change Event A, we tested a new application called `spring-netflix-oss-microservices`. The overall F1 score dropped to 0.744.

One of the main problems we found was that Code2DFD failed to report any of the 17 endpoints in the ground truth. We also found two false connections, including a direction-related issue.

This showed us that the overall F1 score doesn't tell us everything about the tool's performance. We needed a better way to highlight missing endpoints and check whether connections were going in the correct direction.

For M4, we decided to improve our evaluation process rather than change the original Code2DFD tool.

## 2. Possible Solutions

We considered three different options.

| Option | Advantages | Disadvantages | Decision |
|---|---|---|---|
| A. Keep everything the same | No risk of changing existing code or results | Missing endpoints and connection direction issues are not clearly highlighted | Rejected |
| B. Add a separate Python script to check the results | Easy to test, doesn't change original results and highlights potential problems | Some connections still need to be checked manually | Chosen |
| C. Build a larger Adapter system or change Code2DFD | Could be useful for comparing more tools in the future | Would require more work and could introduce unnecessary problems | Rejected |

We chose **Option B** because it addresses the problems we found without making major changes to the project.

It also keeps the new checks separate from the original scoring code, making the system easier to maintain and test.

## 3. What We Implemented

We added a new Python script called `scripts/m4_audit.py`.

The script reads two files from our Change Event A results:

- `eventA/results/final_labels.csv`
- `eventA/results/metrics.csv`

It then performs two main checks.

**Endpoint coverage**

The script checks how many endpoints were present in the ground truth and how many Code2DFD reported.

For Event A, there were 17 endpoints in the ground truth, but Code2DFD reported none.

The script highlights this problem instead of simply showing an overall score. When no endpoints are reported, precision is shown as `null` because it cannot be calculated.

**Connection direction**

The script also checks whether matched connections have been recorded in the wrong direction.

For example, `Service A -> Service B` is different from `Service B -> Service A`.

The script checks for connections that are exactly reversed after basic name formatting. However, if services have different names or aliases, they may still need to be checked manually.

The results are saved in `m4/results/audit.json`.

The new script does not change any of our original labels, precision, recall or F1 scores.

## 4. Testing and Results

We ran the following commands in VS Code:

```bash
python -m unittest discover -s tests -v
python scripts/m4_audit.py
```

All three automated tests passed.

Our results showed:

| Check | Result |
|---|---|
| Automated tests | 3 passed |
| Endpoints in ground truth | 17 |
| Endpoints reported by Code2DFD | 0 |
| Matched connection rows checked | 42 |
| Exact reversed connections detected | 0 |
| Original Event A F1 score | 0.744 |

One of our tests deliberately included a connection going in the wrong direction. The script correctly identified it.

When we ran the script using our actual Event A results, it found no exact reversed connections among the 42 matched rows checked.

This does not mean Code2DFD made no connection errors. We had already identified two false connections during Event A. Our new script only checks for a specific type of direction error.

The original F1 score remained unchanged at 0.744186.

These results show that the additional checks work for the cases we tested without affecting our previous results.

## 5. Limitations

There are still some limitations to our approach.

Firstly, the script uses the labels and results that our group already prepared. It does not independently analyse the original Java application or Code2DFD's raw output.

Secondly, the direction check only identifies connections that are clearly reversed. If services use different names, some connections may still need to be checked manually.

Finally, we have only tested this improvement using our existing Event A results and three automated tests. More testing would be needed before using it across a wider range of applications.

## 6. AI Use

We used AI to help consider possible improvements and develop the Python script and tests.

One suggestion was to build a larger Adapter system. However, we decided this was unnecessary for the problems we had identified.

Instead, we chose a smaller solution that could be tested using our existing data.

We checked the AI-generated code by running three automated tests and executing the script against our Event A results. All three tests passed, and the original F1 score remained unchanged.

The group still needs to review the changes before accepting them as the final M4 work.

## 7. What Still Needs to Be Done

Before starting Change Event B, we need to:

1. Review the new code and results with the group.
2. Confirm that our changes do not conflict with any work completed by other members.
3. Upload the M4 files to GitHub.
4. Update the shared student workbook with our design decision and testing evidence.
5. Create the `PRE_EVENT_B` tag once the group agrees that M4 is complete.

After this, we can begin Change Event B using the completed M4 work as our starting point.

## Conclusion

For M4, we identified weaknesses in how our group was evaluating Code2DFD's results, particularly missing endpoints and connection direction.

We considered three possible solutions and decided that adding a separate Python audit script was the most suitable approach.

The new script makes these issues easier to identify without changing our previous results. All three tests passed, and the Event A F1 score remained unchanged.

We believe this is a suitable improvement because it addresses the problems we found while keeping the changes small and manageable.