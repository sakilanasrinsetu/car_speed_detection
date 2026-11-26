"""Greedy centroid association for the notebook's vehicle detections."""
import math

class Tracker:
    def __init__(self, max_distance=60, max_missed=10):
        self.tracks = {}
        self.next_id = 0
        self.max_distance = max_distance
        self.max_missed = max_missed

    def update(self, boxes):
        centers = [((b[0]+b[2])/2, (b[1]+b[3])/2) for b in boxes]
        pairs = sorted((math.dist(center, state[:2]), i, ident)
                       for i, center in enumerate(centers)
                       for ident, state in self.tracks.items())
        matched, used = {}, set()
        for distance, i, ident in pairs:
            if distance <= self.max_distance and i not in matched and ident not in used:
                matched[i] = ident
                used.add(ident)
        for ident in tuple(self.tracks):
            x, y, missed = self.tracks[ident]
            self.tracks[ident] = (x, y, missed+1)
            if missed+1 > self.max_missed:
                del self.tracks[ident]
        result = []
        for i, box in enumerate(boxes):
            if i not in matched:
                matched[i] = self.next_id
                self.next_id += 1
            ident = matched[i]
            self.tracks[ident] = (*centers[i], 0)
            result.append([*box, ident])
        return result
