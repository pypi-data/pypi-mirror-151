import random
from Classification.InstanceList.Partition cimport Partition
from Classification.Model.Model cimport Model
from Math.DiscreteDistribution cimport DiscreteDistribution
from Classification.Attribute.ContinuousAttribute cimport ContinuousAttribute
from Classification.Attribute.DiscreteAttribute cimport DiscreteAttribute
from Classification.Attribute.DiscreteIndexedAttribute cimport DiscreteIndexedAttribute
from Classification.Instance.CompositeInstance cimport CompositeInstance


cdef class DecisionNode(object):

    EPSILON = 0.0000000001

    def __init__(self, data: InstanceList, condition=None, parameter=None, isStump=False):
        """
        The DecisionNode method takes InstanceList data as input and then it sets the class label parameter by finding
        the most occurred class label of given data, it then gets distinct class labels as class labels ArrayList.
        Later, it adds ordered indices to the indexList and shuffles them randomly. Then, it gets the class distribution
        of given data and finds the best entropy value of these class distribution.

        If an attribute of given data is DiscreteIndexedAttribute, it creates a Distribution according to discrete
        indexed attribute class distribution and finds the entropy. If it is better than the last best entropy it
        reassigns the best entropy, best attribute and best split value according to the newly founded best entropy's
        index. At the end, it also add new distribution to the class distribution.

        If an attribute of given data is DiscreteAttribute, it directly finds the entropy. If it is better than the last
        best entropy it reassigns the best entropy, best attribute and best split value according to the newly founded
        best entropy's index.

        If an attribute of given data is ContinuousAttribute, it creates two distributions; left and right according
        to class distribution and discrete distribution respectively, and finds the entropy. If it is better than the
        last best entropy it reassigns the best entropy, best attribute and best split value according to the newly
        founded best entropy's index. At the end, it also add new distribution to the right distribution and removes
        from left distribution.

        PARAMETERS
        ----------
        data : InstanceList
            InstanceList input.
        condition : DecisionCondition
            DecisionCondition to check.
        parameter : RandomForestParameter
            RandomForestParameter like seed, ensembleSize, attributeSubsetSize.
        isStump : bool
            Refers to decision trees with only 1 splitting rule.
        """
        cdef int bestAttribute, size, j, index, k
        cdef double bestEntropy, entropy, previousValue
        cdef list classLabels, indexList
        cdef DiscreteDistribution classDistribution, distribution, leftDistribution, rightDistribution
        cdef Instance instance
        bestAttribute = -1
        bestSplitValue = 0
        self.__condition = condition
        self.__data = data
        self.__classLabel = Model.getMaximum(self.__data.getClassLabels())
        self.leaf = True
        self.children = []
        classLabels = self.__data.getDistinctClassLabels()
        if len(classLabels) == 1:
            return
        if isStump and condition is not None:
            return
        indexList = [i for i in range(data.get(0).attributeSize())]
        if parameter is not None and parameter.getAttributeSubsetSize() < data.get(0).attributeSize():
            random.seed(parameter.getSeed())
            random.shuffle(indexList)
            size = parameter.getAttributeSubsetSize()
        else:
            size = data.get(0).attributeSize()
        classDistribution = data.classDistribution()
        bestEntropy = data.classDistribution().entropy()
        for j in range(size):
            index = indexList[j]
            if isinstance(data.get(0).getAttribute(index), DiscreteIndexedAttribute):
                for k in range(data.get(0).getAttribute(index).getMaxIndex()):
                    distribution = data.discreteIndexedAttributeClassDistribution(index, k)
                    if distribution.getSum() > 0:
                        classDistribution.removeDistribution(distribution)
                        entropy = (classDistribution.entropy() * classDistribution.getSum() + distribution.entropy() * distribution.getSum()) / data.size()
                        if entropy + self.EPSILON < bestEntropy:
                            bestEntropy = entropy
                            bestAttribute = index
                            bestSplitValue = k
                        classDistribution.addDistribution(distribution)
            elif isinstance(data.get(0).getAttribute(index), DiscreteAttribute):
                entropy = self.__entropyForDiscreteAttribute(index)
                if entropy + self.EPSILON < bestEntropy:
                    bestEntropy = entropy
                    bestAttribute = index
            elif isinstance(data.get(0).getAttribute(index), ContinuousAttribute):
                data.sortWrtAttribute(index)
                previousValue = -100000000
                leftDistribution = data.classDistribution()
                rightDistribution = DiscreteDistribution()
                for k in range(data.size()):
                    instance = data.get(k)
                    if k == 0:
                        previousValue = instance.getAttribute(index).getValue()
                    elif instance.getAttribute(index).getValue() != previousValue:
                        splitValue = (previousValue + instance.getAttribute(index).getValue()) / 2
                        previousValue = instance.getAttribute(index).getValue()
                        entropy = (leftDistribution.getSum() / data.size()) * leftDistribution.entropy() + (rightDistribution.getSum() / data.size()) * rightDistribution.entropy()
                        if entropy + self.EPSILON < bestEntropy:
                            bestEntropy = entropy
                            bestSplitValue = splitValue
                            bestAttribute = index
                    leftDistribution.removeItem(instance.getClassLabel())
                    rightDistribution.addItem(instance.getClassLabel())
        if bestAttribute != -1:
            self.leaf = False
            if isinstance(data.get(0).getAttribute(bestAttribute), DiscreteIndexedAttribute):
                self.__createChildrenForDiscreteIndexed(bestAttribute, bestSplitValue, parameter, isStump)
            elif isinstance(data.get(0).getAttribute(bestAttribute), DiscreteAttribute):
                self.__createChildrenForDiscrete(bestAttribute, parameter, isStump)
            elif isinstance(data.get(0).getAttribute(bestAttribute), ContinuousAttribute):
                self.__createChildrenForContinuous(bestAttribute, bestSplitValue, parameter, isStump)

    cpdef __entropyForDiscreteAttribute(self, int attributeIndex):
        """
        The entropyForDiscreteAttribute method takes an attributeIndex and creates an ArrayList of DiscreteDistribution.
        Then loops through the distributions and calculates the total entropy.

        PARAMETERS
        ----------
        attributeIndex : int
            Index of the attribute.

        RETURNS
        -------
        float
            Total entropy for the discrete attribute.
        """
        cdef double total
        cdef list distributions
        cdef DiscreteDistribution distribution
        total = 0.0
        distributions = self.__data.attributeClassDistribution(attributeIndex)
        for distribution in distributions:
            total += (distribution.getSum() / self.__data.size()) * distribution.entropy()
        return total

    cpdef __createChildrenForDiscreteIndexed(self, int attributeIndex, int attributeValue,
                                           RandomForestParameter parameter, bint isStump):
        """
        The createChildrenForDiscreteIndexed method creates an list of DecisionNodes as children and a partition with
        respect to indexed attribute.

        PARAMETERS
        ----------
        attributeIndex : int
            Index of the attribute.
        attributeValue : int
            Value of the attribute.
        parameter : RandomForestParameter
            RandomForestParameter like seed, ensembleSize, attributeSubsetSize.
        isStump : bool
            Refers to decision trees with only 1 splitting rule.
        """
        cdef Partition childrenData
        childrenData = Partition(self.__data, attributeIndex, attributeValue)
        self.children.append(
            DecisionNode(childrenData.get(0),
                         DecisionCondition(attributeIndex,
                                           DiscreteIndexedAttribute("", attributeValue, self.__data.get(0).getAttribute(attributeIndex).getMaxIndex())), parameter, isStump))
        self.children.append(
            DecisionNode(childrenData.get(1),
                         DecisionCondition(attributeIndex,
                                           DiscreteIndexedAttribute("", -1, self.__data.get(0).getAttribute(attributeIndex).getMaxIndex())), parameter, isStump))

    cpdef __createChildrenForDiscrete(self, int attributeIndex, RandomForestParameter parameter, bint isStump):
        """
        The createChildrenForDiscrete method creates an ArrayList of values, a partition with respect to attributes and
        a list of DecisionNodes as children.

        PARAMETERS
        ----------
        attributeIndex : int
            Index of the attribute.
        parameter : RandomForestParameter
            RandomForestParameter like seed, ensembleSize, attributeSubsetSize.
        isStump : bool
            Refers to decision trees with only 1 splitting rule.
        """
        cdef list valueList
        cdef Partition childrenData
        cdef int i
        valueList = self.__data.getAttributeValueList(attributeIndex)
        childrenData = Partition(self.__data, attributeIndex)
        for i in range(len(valueList)):
            self.children.append(DecisionNode(childrenData.get(i),
                                              DecisionCondition(attributeIndex, DiscreteAttribute(valueList[i])),
                                              parameter, isStump))

    cpdef __createChildrenForContinuous(self, int attributeIndex, double splitValue, RandomForestParameter parameter,
                                      bint isStump):
        """
        The createChildrenForContinuous method creates a list of DecisionNodes as children and a partition with respect
        to continuous attribute and the given split value.

        PARAMETERS
        ----------
        attributeIndex : int
            Index of the attribute.
        parameter : RandomForestParameter
            RandomForestParameter like seed, ensembleSize, attributeSubsetSize.
        isStump : bool
            Refers to decision trees with only 1 splitting rule.
        splitValue : float
            Split value is used for partitioning.
        """
        cdef Partition childrenData
        childrenData = Partition(self.__data, attributeIndex, splitValue)
        self.children.append(DecisionNode(childrenData.get(0),
                                          DecisionCondition(attributeIndex, ContinuousAttribute(splitValue), "<"),
                                          parameter, isStump))
        self.children.append(DecisionNode(childrenData.get(1),
                                          DecisionCondition(attributeIndex, ContinuousAttribute(splitValue), ">"),
                                          parameter, isStump))

    cpdef str predict(self, Instance instance):
        """
        The predict method takes an Instance as input and performs prediction on the DecisionNodes and returns the
        prediction for that instance.

        PARAMETERS
        ----------
        instance : Instance
            Instance to make prediction.

        RETURNS
        -------
        str
            The prediction for given instance.
        """
        cdef list possibleClassLabels
        cdef DiscreteDistribution distribution
        cdef str predictedClass, childPrediction
        cdef DecisionNode node
        if isinstance(instance, CompositeInstance):
            possibleClassLabels = instance.getPossibleClassLabels()
            distribution = self.__data.classDistribution()
            predictedClass = distribution.getMaxItemIncludeTheseOnly(possibleClassLabels)
            if self.leaf:
                return predictedClass
            else:
                for node in self.children:
                    if node.__condition.satisfy(instance):
                        childPrediction = node.predict(instance)
                        if childPrediction is not None:
                            return childPrediction
                        else:
                            return predictedClass
                return predictedClass
        elif self.leaf:
            return self.__classLabel
        else:
            for node in self.children:
                if node.__condition.satisfy(instance):
                    return node.predict(instance)
            return self.__classLabel

    cpdef dict predictProbabilityDistribution(self, Instance instance):
        cdef DecisionNode node
        if self.leaf:
            return self.__data.classDistribution().getProbabilityDistribution()
        else:
            for node in self.children:
                if node.__condition.satisfy(instance):
                    return node.predictProbabilityDistribution(instance)
            return self.__data.classDistribution().getProbabilityDistribution()
