
import faiss


def save_index(index,path):

    faiss.write_index(index,path)



def load_index(path):

    return faiss.read_index(path)
