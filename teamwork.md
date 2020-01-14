# Teamwork Reflection

![Agile Scrum Diagram](https://brainhub.eu/blog/wp-content/uploads/2018/04/differences-lean-agile-scrum-scrum-process.jpg)

## Overview & Goal
The <b>ultimate goal</b> for teamwork in this project was to put the agile scrum process into practice. This meant simulating and/or using <b>sprints, backlogs and standups</b> to maximise our efficiency as a team in producing the final product. The method by which we achieved this evolved continuously throughout the <b>software development lifecycle</b>, with our <b>productivity</b> correspondingly increasing with each iteration.

## Communication
<i>How often you met, and why you met that often</i>; <i>What methods you used to ensure that meetings were successful</i>

### Discord & Screen Share
![Discord & Screen Share](https://i.imgur.com/LHt8C0a.png)
<b>Discord</b> is a VOIP application designed for text and audiovisual communication within teams. Whilst other applications such as Slack and Messenger were considered, it was ultimately decided that Slack lacked accessibility for certain members of the team, and Messenger lacked integral features for maximum productivity such as screen share. Such consideration of <b>accessibility</b> and <b>open-minded approach</b> to trying out different communication mediums reflects how each and every member of the team was actively involved in the <b>decision-making process</b>; and contributed to our offline meetings being successful each time.

In particular, the team's use of Discord's <b>screen share</b> feature allowed the team to <b>simulate a face-to-face meeting</b>, wherein each team member could actively collaborate with each other and solve problems more efficiently through <b>transparency</b> and by always being on the same page.

### In-Person Meetings
Apart from the <b>weekly labs</b> on Thursday, wherein the team had the ability to discuss any major issues with the course tutor and lab assistant, the team also regularly met for <b>2 - 3 hours</b> every Wednesday evening. UNSW was selected as the location of such meetings for <b>geographical neutrality</b> between the team. As the team was consistently working together under simulated in-person meeting conditions (on Discord), this periodicity of the meeting was more than enough to get through any <b>major hurdles</b> together and discuss what each member of the team will be tackling that week.

The aim of these meetings was to <b>simulate a weekly standup</b>, wherein the team could all be brought back on to the same page, which maximised the coherency in discussions and the productivity of each member overall.

<b>During the meetings</b> themselves, the team ensured successful communication by practicing:
- <b>Active listening</b>: restating, reflecting and summarising the speaker's major points
- <b>Conflict resolution & negotiation</b>: being open to new and different opinions
- <b>Team building</b>: ensuring every member of the team feels included

In addition, the team reconvened again on numerous occasions outside of these regular meeting times for urgent discussions; which demonstrates the <b>flexibility</b> this team could exhibit by the end of this project.

## Response to Unexpected Events
<i>What steps you took when things did not go to plan during iteration 3</i>

Whenever a team member encountered an issue while working on Iteration 3, we took steps as a team to help alleviate that issue. Throughout the project, we maintained multiple open and active communication channels, where each member would keep the team updated on their progress. Despite working closely together throughout Iteration 3, we ran into some unexpected events.

For instance, there were some programming issues with `search.py`, which we discovered when attempting to achieve total branch coverage. The issue was that when we ran `pytest` on `search_test.py`, there would be no problems. However, we did not realise that it wasn't producing the correct output. In response to this, we identified and rectified the issue, and tested it thoroughly to ensure a correct output. In addition, we added the tests that would ensure that the `search` function would work as intended. Coincidentally, two members found and resolved the issue independently, but on different branches.

This was unexpected, namely the fact that team members were sometimes working on the same file or function, but on different branches. Naturally, when merging, this would result in confusion due to merge conflicts with similar code, causing stress over whether accepting a change might backtrack our progress. In resolving this, the team members who worked on the file would discuss with each other what they did and any issues they had. After examining the difference between the two files, the team members would implement the best solution, and consider the ability of the code to satisfy the project specifications, and considering the SE principles implemented within it.

A last example of how we responded to unexpected events was during the implementation of pytest fixtures. We had implemented fixtures, and all the tests passed, so the team assumed that we had implemented them correctly. However, unknowing at first, we found that the fixtures were not running at all. Upon discovering this, the team rectified the issue, to further strengthen the tests.

## Collaboration
<i>Details on how you had multiple people working on the same code</i>

### Git
![gitgraph Command](https://i.imgur.com/JBKB27h.png)

<b>Git</b> is a distributed version-control system for <b>tracking changes</b> and <b>coordinating work</b> within a team. Especially as a mostly online team, Git (and Gitlab, which is a web interface for a Git repository) allowed the team to work on the same file concurrently to promote productivity without unintentionally disrupt each other's code flow. In addition, Git's ability to save commits with messages, and the team's dedication in providing <b>detailed commit logs</b> have allowed team members to quickly pick up where another team member left a particular task.

Only in the most complex of cases did the team member have to clarify the changes made by another team member.

### User Stories Backlog
![User Stories](https://i.imgur.com/yp7Qs5a.png)

The <b>user stories backlog</b> simulated using the issues board on GitLab enabled team members to clearly see which user stories were addressed, in the process of addressing, and must be addressed in the future. Not only did this successfully signpost and <b>guide what each team member must be working on at any one point in time</b>, it allowed the team to <b>track each others' progress</b> and <b>see the bigger picture</b> we are working towards as a whole.

### Standups

<b>Standup meetings</b> are short, 15 minute meetings wherein each team member updates the rest of the team on their progress and what they will be working on next, along with what they are currently stuck on. As such a physical meeting was impractical given the nature of the task and geographical location of each member, we simulated standup meetings on Discord, wherein we would stop working (hence the standup being synchronous) to update each other on their status and blockages regarding their task. This resulted in the team always <b>working on the same page</b> with no team member being left behind or acting without the rest of the team being aware of the changes being made. This cohesion is one of the elements which contributed to this team's success.

### Pair Programming
![Pair Programming](https://i.imgur.com/lU6uQal.png)

<b>Pair programming</b> is a method of collaborative programming wherein two individuals work on a single programming problem together; consulting and guiding each other in the process. For particularly <b>difficult problems and/or features</b> encountered during the development process, the team split into two groups on Discord; with each pair working on that one problem together collaboratively (once again, through the share screen feature). This significantly improved the team's <b>problem solving</b> abilities; enabling challenges to be overcome and productivity to reach its peak.