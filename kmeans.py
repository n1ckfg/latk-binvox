# based on https:#openprocessing.org/sketch/51404/

class Kmeans(object):
	def __init__(self, _points, _numCentroids): # ArrayList<PVector>, int
	    self.particles = [] # ArrayList<Particle>
	    self.centroids = [] # ArrayList<Centroid>
	    self.centroidFinalPositions = [] # ArrayList<PVector>
	    self.clusters = [] # ArrayList<Cluster>
	    
	    self.numberOfCentroids = _numCentroids # int
	    self.minX = 0.0
	    self.maxX = 0.0
	    self.minY = 0.0
	    self.maxY = 0.0
	    self.minZ = 0.0
	    self.maxZ = 0.0
	    self.totalStability = 0.0
	    self.stableThreshold = 0.0001
	    self.ready = False
        
        for i in range(0, len(_points)):
            p = _points[i] # PVector
            if (p.x < minX) minX = p.x
            if (p.x > maxX) maxX = p.x
            if (p.y < minY) minY = p.y
            if (p.y > maxY) maxY = p.y
            if (p.z < minZ) minZ = p.z
            if (p.z > maxZ) maxZ = p.z
            particles.append(Particle(p))
        
        self.init()
    
    def init(self):    
        self.ready = False
        self.centroids.clear()
        self.clusters.clear()
    
        for i in range(0, self.numberOfCentroids):
            c = Centroid(i, 127+random(127), 127+random(127), 127+random(127), self.minX, self.maxX, self.minY, self.maxY, self.minZ, self.maxZ)
            centroids.append(c)
        
    def update(self):
        for particle in self.particles: 
            particle.FindClosestCentroid(self.centroids)
        
        self.totalStability = 0
        
        for centroid in self.centroids:
            centroid.update(self.particles)
            if (centroid.stability > 0) self.totalStability += centroid.stability
        
        if (self.totalStability < self.stableThreshold):
            for centroid in self.centroids:
                p = centroid.position # PVector
                self.clusters.append(Cluster(p))
                self.centroidFinalPositions.append(p)
            
            for particle in self.particles:
                self.clusters.get(particle.centroidIndex).points.append(particle.position)
            
            self.ready = True
        
        #println(totalStability + " " + ready)
    
    '''
    def draw(self):
        if (self.ready == False):
            for particle in self.particles:
                particle.draw()
        
            for centroid in self.centroids:
                centroid.draw()
    '''

    def run(self):
        if (self.ready == False):
        	self.update()
        #self.draw()
 
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

class Centroid(object):
	def __init__(self, _internalIndex, _r, _g, _b, _minX, _maxX, _minY, _maxY, _minZ, _maxZ): # int, float, float, float, float, float, float, float, float, float
	    self.position = (random(_minX, _maxX), random(_minY, _maxY), random(_minZ, _maxZ))
	    self.colorR = _r
	    self.colorG = _g
	    self.colorB = _b
	    self.internalIndex = _internalIndex
	    self.stability = -1.0

    def update(self, _particles): # ArrayList<Particle>
        #println("-----------------------")
        #println("K-Means Centroid Tick")
        # move the centroid to its position

        newPosition = (0.0, 0.0, 0.0)

        numberOfAssociatedParticles = 0

        for curParticle in _particles:
            if (curParticle.centroidIndex == self.internalIndex):
                newPosition[0] += curParticle.position[0]
                newPosition[1] += curParticle.position[1]
                newPosition[2] += curParticle.position[2]
                numberOfAssociatedParticles += 1

        newPosition = (newPosition[0] / numberOfAssociatedParticles, newPosition[1] / numberOfAssociatedParticles, newPosition[2] / numberOfAssociatedParticles)
        self.stability = dist(position, newPosition)
        self.position = newPosition

    '''
    def draw(self):
        pushMatrix()
        translate(position.x, position.y, position.z)
        strokeWeight(10)
        stroke(colorR, colorG, colorB)
        point(0,0)
        popMatrix()
    '''

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

class Particle(object):
	def __init__(self, _position): # PVector
	    self.position = _position # PVector
	    self.velocity # PVector
	    self.centroidIndex # int
	    self.colorR # float
	    self.colorG # float
	    self.colorB # float
	    self.brightness = 0.8
    
    def FindClosestCentroid(self, _centroids): # ArrayList<Centroid> 
        closestCentroidIndex = 0 # int
        closestDistance = 100000.0

        # find which centroid is the closest
        for i in range(0, len(_centroids)):             
            curCentroid = _centroids[i] # Centroid

            distanceCheck = dist(position, curCentroid.position) # float

            if (distanceCheck < closestDistance):
                closestCentroidIndex = i
                closestDistance = distanceCheck

        # now that we have the closest centroid chosen, assign the index,
        self.centroidIndex = closestCentroidIndex

        # and grab the color for the visualization        
        curCentroid = _centroids[centroidIndex] # Centroid 
        self.colorR = curCentroid.colorR * self.brightness
        self.colorG = curCentroid.colorG * self.brightness
        self.colorB = curCentroid.colorB * self.brightness
    
    '''
    def draw(self):
        pushMatrix()
        translate(position.x, position.y, position.z)
        strokeWeight(2)
        stroke(colorR, colorG, colorB)
        point(0, 0)
        popMatrix()
    '''

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

 class Cluster(object):
 	def __init__(self, _centroid): # PVector    
        self.centroid = _centroid
        self.points = []
     
     
 