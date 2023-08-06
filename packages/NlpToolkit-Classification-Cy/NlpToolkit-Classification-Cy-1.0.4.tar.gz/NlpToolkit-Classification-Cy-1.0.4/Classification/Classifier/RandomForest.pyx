from Classification.Classifier.Classifier cimport Classifier
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Model.DecisionTree.DecisionNode cimport DecisionNode
from Classification.Model.DecisionTree.DecisionTree cimport DecisionTree
from Classification.Model.TreeEnsembleModel cimport TreeEnsembleModel
from Classification.Parameter.Parameter cimport Parameter
from Sampling.Bootstrap cimport Bootstrap


cdef class RandomForest(Classifier):

    cpdef train(self, InstanceList trainSet, Parameter parameters):
        """
        Training algorithm for random forest classifier. Basically the algorithm creates K distinct decision trees from
        K bootstrap samples of the original training set.

        PARAMETERS
        ----------
        trainSet : InstanceList
            Training data given to the algorithm
        parameters : RandomForestParameter
            Parameters of the bagging trees algorithm. ensembleSize returns the number of trees in the random forest.
        """
        cdef int forestSize, i
        cdef list forest
        cdef Bootstrap bootstrap
        cdef DecisionTree tree
        forestSize = parameters.getEnsembleSize()
        forest = []
        for i in range(forestSize):
            bootstrap = trainSet.bootstrap(i)
            tree = DecisionTree(DecisionNode(InstanceList(bootstrap.getSample()), None, parameters, False))
            forest.append(tree)
        self.model = TreeEnsembleModel(forest)
