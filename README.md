# discovery

Can we enable Mistral models to perform drug discovery? LLMs have already shown [promise](https://github.com/ur-whitelab/chemcrow-public) in this area, but if models cannot already solve this problem, what intervention could we impose to enable them to do so? While Mistral models are pretrained, they can be post-trained via [in-context learning](https://arxiv.org/abs/2005.14165) or finetuning. Following [(Udandarao et al., 2024)](https://arxiv.org/abs/2404.04125), we look to answer this question by tying the drug discovery task to what Mistral models are post-trained on, and laid the groundwork for doing so in this hackathon. 

## test task(s)

We identified two candidate testsets for assessing performance, structure-based drug discovery (SBDD), where the task is to design a molecule that binds to a target protein, and text-to-protein (T2P), where the task is to retrieve or generate a protein given a text prompt. For SBDD, we created the `PocketLigandPairDataset` with the following command,
```bash
python -m utils.datasets.pl data/crossdocked_pocket10
```
using the [Pocket2Mol](https://github.com/pengxingang/Pocket2Mol) dataset creation scripts. For T2P, we simply download `uniprot_sprot*` from [here](https://zenodo.org/records/11176863). We decided to proceed with the T2P task given its user-friendly nature and since Mistral's models are designed to handle text. 

## preliminary results

### mistral-embed
For T2P retrieval, text embeddings and protein embeddings must align, but protein embeddings come from protein models, such as [ESM](https://github.com/facebookresearch/esm/tree/main). Hence, we would need to align them, but given Mistral does not provide the finetune feature for embedding models, we proceed using custom tools. For this, we run, 
```bash
python bin/train_protein_clip.py configs/clip_hparams.json data/uniprot_sprot.dat.gz data/esm_6layer.hdf5 --unitnorm
```
using the [ProteinCLIP](https://github.com/wukevin/proteinclip) training script. However, due to request rate limits, this proved intractable to run on our own compute in the course of the hackathon. 
### mistral large 2
For T2P generation, one will only truly know if the generated protein adheres to the desired prompt upon synthesis in a lab, e.g. using synthesis and characterization platforms. However, one can computationally evaluate using "in-silico" metrics, such as AlphaFold confidence, measured using open-source tools like [OmegaFold](https://github.com/HeliXonProtein/OmegaFold). Still, there is the challenge of restricting the LLM to adhere to a specified format, free-form generation can lead to valid answers such as to simply find the protein sequence associated with a certain protein functions using search engines such as Google search. A simple way to specify the format is to use multiple-choice question answering, however true discovery tasks cannot be represented in such a way in practice. Thus, in the absence of a wetlab, our evaluation will only be a proxy of the true one, which is used to build confidence in candidate generation before the true evaluation. 
