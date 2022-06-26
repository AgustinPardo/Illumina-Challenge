class Region:
    """Class to store region info"""

    def __init__(self, y_axis, start, stop):

        self.y_axis = y_axis
        self.start = start
        self.stop = stop

    def to_string(self):
        """Return region info as string"""

        line = list(map(str, [self.y_axis, self.start, self.stop]))
        return ('\t'.join(line) + '\n')

    def to_list(self):
        """Return region info as list"""

        return [self.y_axis, self.start, self.stop]


class Segment:
    """Class to store segment info"""

    def __init__(self, count, start, stop):

        self.count = count
        self.start = start
        self.stop = stop

    def to_string(self):
        """Return segment info as string"""
        
        line = list(map(str, [self.count, self.start, self.stop]))
        return ('\t'.join(line) + '\n')

    def to_list(self):
        """Return segment info as string"""

        return [self.count, self.start, self.stop]


class Parser:
    """Class to get and parse data from source file"""

    def __init__(self, data_path):

        self.data_path = data_path
        # Store regions in a list of Region objects
        self.regions = []
        # Store segments in a list of Segment objects
        self.segments = []

        self.get_data()
        self.non_overlapping_segments()

    def get_data(self):
        """Read source file and create regions and segments datasets"""

        regions_file = open(self.data_path, 'r')
        regions_lines = regions_file.readlines()
        regions_file.close()

        for line in regions_lines:
            split_line = line.rstrip().split('\t')
            start = int(split_line[0])
            stop = int(split_line[1])
            region = Region(0, start, stop)
            self.regions.append(region)
            self.segments = self.segments + [start, stop]

    def non_overlapping_segments(self):
        """Parse segments dataset as a list of non-overlapping Segment intervals"""

        # Remove duplicated segments to avoid duplicated non-overlapping intervals
        self.segments = list(set(self.segments))
        # Order the segments to set correctly non-overlapping interval
        self.segments.sort()
        # Set non-overlapping intervals as region-region start-stop pairs Segment objects
        # If segment B has start position X, then segment A has end position X-1. The segments do not overlap.
        self.segments = [Segment(0, self.segments[i], self.segments[i + 1] - 1) for i in range(len(self.segments)-1)]
      

class Process:
    """Class to process part1 and part2 tasks and export results"""

    def __init__(self, regions, segments):

        self.regions = regions
        self.segments = segments

    def to_list(self, dataset):
        """Return dataset(Region/Segment) as a list of list info"""

        return [data.to_list() for data in dataset]

    def export_data(self, dataset, path):
        """Export results to output file"""

        output = open(path, 'w')
        for data in dataset:
            output.write(data.to_string())
        output.close()

    def overlap(self, region1, region2):
        """Check if two region/segment overlaps"""

        # Overlap border cases consideration:
        # If the overlap is based on 1 position been a START ovelap over a STOP, is not considered overlap
        return ((region1.start <= region2.start < region1.stop) or 
                (region1.start < region2.stop <= region1.stop) or 
                ((region1.start >= region2.start) and (region1.stop <= region2.stop)))

    def part1_task(self):
        """Part1 task calculation"""

        for region in self.regions:
            # Store the Y-axis level used by other regions on the start-stop coordinates scope
            overlaped_y_axis = []
            for comp_region in self.regions:                
                if self.overlap(comp_region, region):
                    overlaped_y_axis.append(comp_region.y_axis)

            overlaped_y_axis.sort()
            # Select the highest Y-axis level in used and add 1
            updated_y_axis = overlaped_y_axis[-1] + 1
            # Check if there is and empty lower level. If there are more than one select the lowest
            i = 0
            while i < len(overlaped_y_axis)-1:
                if overlaped_y_axis[i+1] > overlaped_y_axis[i] + 1:
                    updated_y_axis = overlaped_y_axis[i] + 1
                    break
                i+=1
            # Update the region Y-axis level value
            region.y_axis = updated_y_axis

    def part2_task(self):
        """Part2 task calculation"""

        for segment in self.segments:
            for region in self.regions:
                if self.overlap(segment, region):
                    # If a region overlap the segment add 1 to segment count
                    segment.count += 1
        # Remove segments with no overlapping regions
        self.segments = [segment for segment in self.segments if segment.count>0]
