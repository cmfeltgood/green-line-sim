# Green Line Simulator

The MBTA Green Line is known for being quite slow compared to the rest of the agency's transit. I would attribute that fact to the desnity of trains in the main tunnel, density of stops, and being stuck in car traffic signals.

I want to simulate how the green line works to figure out what changes to the way the line works cause a faster line, and by how much. As a start, I'm only modeling the C branch, the shortest and simplest branch.

This is the third revision of this project, the first getting dropped after making very clunky code over a summer, and the second being lost to an overwritten flash drive. I have learned my lesson.

### Done so far

- Get Beacon St intersection data
- Make a train!
- Have the train go forward on a basic track
- Make tracks for intersections
- Make tracks for stations (basic 10 second timer for now)

### To-Do

- Combine my data with the MBTA's intersection data
- Create a data importer for the combined track data
- Export tests from multiple runs.
- Check for accuracy of train running times
- *If innacurate, consider optional steps below*
- Create test cases for changes to the branch
- Compare data from test cases

### Optional, for more accurate trains

- Add more logic for station stop times
- Nudge acceleration/decceleration rates

## After C Branch Test

- Allow for tracks to separate/merge
- Make trains stop for each other
- Collect a boatload more data
