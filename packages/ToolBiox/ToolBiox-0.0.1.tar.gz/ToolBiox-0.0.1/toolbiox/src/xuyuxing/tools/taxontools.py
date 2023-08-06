from api.common.genome.blast import outfmt6_read_big
from lib.xuyuxing.evolution.taxonomy import build_taxon_database, blast_taxon_assign, get_common_tree
from lib.common.os import multiprocess_running


def DiamondTaxonAssign_main(args):
    taxon_dict = build_taxon_database(args.tax_dir)

    args_list = []
    args_id_list = []
    for query_record in outfmt6_read_big(args.blast_results,
                                            fieldname=["qseqid", "sseqid", "staxids", "pident", "length",
                                                    "mismatch",
                                                    "gapopen", "qstart", "qend", "sstart", "send", "evalue",
                                                    "bitscore"]):

        query_name = query_record.qDef

        taxon_score_list = []
        for hit_tmp in query_record.hit:
            for taxon in hit_tmp.Hit_taxon_id:
                if taxon == '':
                    continue
                if taxon is None:
                    continue
                score = hit_tmp.hsp[0].Hsp_bit_score
                taxon_score_list.append((taxon, score))

        taxon_id_list = list(set([i[0] for i in taxon_score_list]))

        if taxon_id_list == []:
            continue

        common_tree = get_common_tree(taxon_id_list, taxon_dict)

        # root_taxon, fisher_taxon, q_value = blast_taxon_assign(taxon_score_list, taxon_dict, True)

        args_list.append((taxon_score_list, common_tree))
        args_id_list.append(query_name)

    cmd_result = multiprocess_running(blast_taxon_assign, args_list, args.num_threads, args_id_list=args_id_list)

    with open(args.output_file, 'w') as f:
        for query_id in args_id_list:
            if cmd_result[query_id]['output'] == "bug":
                print(query_id)
            else:
                root_taxon, fisher_taxon, q_value = cmd_result[query_id]['output']
                f.write("%s\t%s\t%s\t%s\t%s\t%.5f\n" % (
                    query_id, root_taxon, taxon_dict[root_taxon].sci_name, fisher_taxon,
                    taxon_dict[fisher_taxon].sci_name, q_value))
