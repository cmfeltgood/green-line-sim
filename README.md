# Green Line Simulator

The MBTA Green Line is known for being quite slow compared to the rest of the agency's transit. I would attribute that fact to the desnity of trains in the main tunnel, density of stops, and being stuck in car traffic signals.

I want to simulate how the green line works to figure out what changes to the way the line works cause a faster line, and by how much. As a start, I'm only modeling the C branch, the shortest and simplest branch.

This is the third revision of this project, the first getting dropped after making very clunky code over a summer, and the second being lost to an overwritten flash drive. I have learned my lesson.

## Update 3/25/25

The model is now fully functional for one branch and one train at a time, 
with a relatively accurate median (about 30 seconds fast, which is good enough for now). 
Making there be multiple trains should be relatively easy, 
although I need logic to be sure trains don't run into each other, 
or especially pass each other.

The extremities don't currently match real data though. 
I don't care to model if a train needs to stop for anything other than lights and passengers, 
so the max won't really match, but the min would be affected by a lack of passengers at stations.

Next steps are to:
- Get more accurate station stop times, with predictions on how # passengers affects dwells
- Have stop times change based on time of day and time since last train
- Allow for multiple trains on one track by only allowing one train in a station
- * Note: I think this should prevent trains from moving into eachother. If this is false, I'll add more logic
- At some point get data exported, with more info on times spent stopped, at full speed, etc.
- Create more test cases

### Done so far

- Get Beacon St intersection data
- Make a train!
- Have the train go forward on a basic track
- Make tracks for intersections
- Make tracks for stations (basic 10 second timer for now)
- Combine my intersection data with the MBTA's data
- Create a data importer for the combined track data
- Check for accuracy of train running times

### To-Do

- Add more logic for station stop times
- Allow for multiple trains on the tracks
- Export tests from multiple runs.
- Create test cases for changes to the branch
- Compare data from test cases



## After C Branch Test

- Allow for tracks to separate/merge
- Make trains stop for each other
- Collect a boatload more data
