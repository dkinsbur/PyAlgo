import xml.etree.ElementTree as ET

html = r"""
<tbody>
                <tr id="historicEvent_347347" event_attr_id="75" event_timestamp="2017-04-19 14:30:00">
            <td class="left">Apr 19, 2017 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">-1.034M</span></td>
                <td class="noWrap">-1.470M</td>
                <td class="blackFont noWrap">-2.166M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_346987" event_attr_id="75" event_timestamp="2017-04-12 14:30:00">
            <td class="left">Apr 12, 2017 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">-2.166M</span></td>
                <td class="noWrap">0.087M</td>
                <td class="blackFont noWrap">1.566M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_346665" event_attr_id="75" event_timestamp="2017-04-05 14:30:00">
            <td class="left">Apr 05, 2017 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">1.566M</span></td>
                <td class="noWrap">-0.435M</td>
                <td class="blackFont noWrap">0.867M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_346356" event_attr_id="75" event_timestamp="2017-03-29 14:30:00">
            <td class="left">Mar 29, 2017 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">0.867M</span></td>
                <td class="noWrap">1.357M</td>
                <td class="blackFont noWrap">4.954M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_345961" event_attr_id="75" event_timestamp="2017-03-22 14:30:00">
            <td class="left">Mar 22, 2017 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">4.954M</span></td>
                <td class="noWrap">2.801M</td>
                <td class="blackFont noWrap">-0.237M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
        <tr id="historicEvent_345568" event_attr_id="75" event_timestamp="2017-03-15 14:30:00">
            <td class="left">Mar 15, 2017 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">-0.237M</span></td>
                <td class="noWrap">3.713M</td>
                <td class="blackFont noWrap">8.209M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_345260" event_attr_id="75" event_timestamp="2017-03-08 15:30:00">
            <td class="left">Mar 08, 2017 </td>
            <td class="left">11:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">8.209M</span></td>
                <td class="noWrap">1.967M</td>
                <td class="blackFont noWrap">1.501M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_344700" event_attr_id="75" event_timestamp="2017-03-01 15:30:00">
            <td class="left">Mar 01, 2017 </td>
            <td class="left">11:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">1.501M</span></td>
                <td class="noWrap">3.079M</td>
                <td class="blackFont noWrap">0.564M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_344542" event_attr_id="75" event_timestamp="2017-02-23 16:00:00">
            <td class="left">Feb 23, 2017 </td>
            <td class="left">12:00</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">0.564M</span></td>
                <td class="noWrap">3.475M</td>
                <td class="blackFont noWrap">9.527M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_344131" event_attr_id="75" event_timestamp="2017-02-15 15:30:00">
            <td class="left">Feb 15, 2017 </td>
            <td class="left">11:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">9.527M</span></td>
                <td class="noWrap">3.513M</td>
                <td class="blackFont noWrap">13.830M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_343694" event_attr_id="75" event_timestamp="2017-02-08 15:30:00">
            <td class="left">Feb 08, 2017 </td>
            <td class="left">11:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">13.830M</span></td>
                <td class="noWrap">2.529M</td>
                <td class="blackFont noWrap">6.466M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr><tr id="historicEvent_343379" event_attr_id="75" event_timestamp="2017-02-01 15:30:00">
            <td class="left">Feb 01, 2017 </td>
            <td class="left">11:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">6.466M</span></td>
                <td class="noWrap">3.289M</td>
                <td class="blackFont noWrap">2.840M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_342002" event_attr_id="75" event_timestamp="2017-01-25 15:30:00">
            <td class="left">Jan 25, 2017 </td>
            <td class="left">11:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">2.840M</span></td>
                <td class="noWrap">2.815M</td>
                <td class="blackFont noWrap">2.347M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_341395" event_attr_id="75" event_timestamp="2017-01-19 16:00:00">
            <td class="left">Jan 19, 2017 </td>
            <td class="left">12:00</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">2.347M</span></td>
                <td class="noWrap">-0.342M</td>
                <td class="blackFont noWrap">4.097M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_341012" event_attr_id="75" event_timestamp="2017-01-11 15:30:00">
            <td class="left">Jan 11, 2017 </td>
            <td class="left">11:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">4.097M</span></td>
                <td class="noWrap">1.162M</td>
                <td class="blackFont noWrap">-7.051M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_340696" event_attr_id="75" event_timestamp="2017-01-05 16:00:00">
            <td class="left">Jan 05, 2017 </td>
            <td class="left">12:00</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">-7.051M</span></td>
                <td class="noWrap">-2.152M</td>
                <td class="blackFont noWrap">0.614M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_340304" event_attr_id="75" event_timestamp="2016-12-29 16:00:00">
            <td class="left">Dec 29, 2016 </td>
            <td class="left">12:00</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">0.614M</span></td>
                <td class="noWrap">-2.060M</td>
                <td class="blackFont noWrap">2.256M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr><tr id="historicEvent_340008" event_attr_id="75" event_timestamp="2016-12-21 15:30:00">
            <td class="left">Dec 21, 2016 </td>
            <td class="left">11:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">2.256M</span></td>
                <td class="noWrap">-2.515M</td>
                <td class="blackFont noWrap">-2.563M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_339721" event_attr_id="75" event_timestamp="2016-12-14 15:30:00">
            <td class="left">Dec 14, 2016 </td>
            <td class="left">11:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">-2.563M</span></td>
                <td class="noWrap">-1.584M</td>
                <td class="blackFont noWrap">-2.389M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_339284" event_attr_id="75" event_timestamp="2016-12-07 15:30:00">
            <td class="left">Dec 07, 2016 </td>
            <td class="left">11:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">-2.389M</span></td>
                <td class="noWrap">-1.032M</td>
                <td class="blackFont noWrap">-0.884M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_338943" event_attr_id="75" event_timestamp="2016-11-30 15:30:00">
            <td class="left">Nov 30, 2016 </td>
            <td class="left">11:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">-0.884M</span></td>
                <td class="noWrap">0.636M</td>
                <td class="blackFont noWrap">-1.255M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_338594" event_attr_id="75" event_timestamp="2016-11-23 15:30:00">
            <td class="left">Nov 23, 2016 </td>
            <td class="left">11:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">-1.255M</span></td>
                <td class="noWrap">0.671M</td>
                <td class="blackFont noWrap">5.274M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_338174" event_attr_id="75" event_timestamp="2016-11-16 15:30:00">
            <td class="left">Nov 16, 2016 </td>
            <td class="left">11:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">5.274M</span></td>
                <td class="noWrap">1.480M</td>
                <td class="blackFont noWrap">2.432M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr><tr id="historicEvent_337807" event_attr_id="75" event_timestamp="2016-11-09 15:30:00">
            <td class="left">Nov 09, 2016 </td>
            <td class="left">11:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">2.432M</span></td>
                <td class="noWrap">1.330M</td>
                <td class="blackFont noWrap">14.420M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_337480" event_attr_id="75" event_timestamp="2016-11-02 14:30:00">
            <td class="left">Nov 02, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">14.420M</span></td>
                <td class="noWrap">1.013M</td>
                <td class="blackFont noWrap">-0.553M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_337127" event_attr_id="75" event_timestamp="2016-10-26 14:30:00">
            <td class="left">Oct 26, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">-0.553M</span></td>
                <td class="noWrap">1.699M</td>
                <td class="blackFont noWrap">-5.200M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_336737" event_attr_id="75" event_timestamp="2016-10-19 14:30:00">
            <td class="left">Oct 19, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">-5.247M</span></td>
                <td class="noWrap">2.705M</td>
                <td class="blackFont noWrap">4.900M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_336309" event_attr_id="75" event_timestamp="2016-10-13 15:00:00">
            <td class="left">Oct 13, 2016 </td>
            <td class="left">11:00</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">4.900M</span></td>
                <td class="noWrap">0.650M</td>
                <td class="blackFont noWrap">-2.976M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_335988" event_attr_id="75" event_timestamp="2016-10-05 14:30:00">
            <td class="left">Oct 05, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">-2.976M</span></td>
                <td class="noWrap">2.560M</td>
                <td class="blackFont noWrap">-1.882M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr><tr id="historicEvent_335620" event_attr_id="75" event_timestamp="2016-09-28 14:30:00">
            <td class="left">Sep 28, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">-1.882M</span></td>
                <td class="noWrap">2.995M</td>
                <td class="blackFont noWrap">-6.200M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_335274" event_attr_id="75" event_timestamp="2016-09-21 14:30:00">
            <td class="left">Sep 21, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">-6.200M</span></td>
                <td class="noWrap">3.350M</td>
                <td class="blackFont noWrap">-0.559M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_334978" event_attr_id="75" event_timestamp="2016-09-14 14:30:00">
            <td class="left">Sep 14, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">-0.559M</span></td>
                <td class="noWrap">3.800M</td>
                <td class="blackFont noWrap">-14.513M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_334552" event_attr_id="75" event_timestamp="2016-09-08 15:00:00">
            <td class="left">Sep 08, 2016 </td>
            <td class="left">11:00</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">-14.513M</span></td>
                <td class="noWrap">0.225M</td>
                <td class="blackFont noWrap">2.276M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_334278" event_attr_id="75" event_timestamp="2016-08-31 14:30:00">
            <td class="left">Aug 31, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">2.276M</span></td>
                <td class="noWrap">0.921M</td>
                <td class="blackFont noWrap">2.501M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_333899" event_attr_id="75" event_timestamp="2016-08-24 14:30:00">
            <td class="left">Aug 24, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">2.501M</span></td>
                <td class="noWrap">-0.455M</td>
                <td class="blackFont noWrap">-2.508M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr><tr id="historicEvent_333511" event_attr_id="75" event_timestamp="2016-08-17 14:30:00">
            <td class="left">Aug 17, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">-2.508M</span></td>
                <td class="noWrap">0.522M</td>
                <td class="blackFont noWrap">1.055M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_333167" event_attr_id="75" event_timestamp="2016-08-10 14:30:00">
            <td class="left">Aug 10, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">1.055M</span></td>
                <td class="noWrap">-1.025M</td>
                <td class="blackFont noWrap">1.413M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_332797" event_attr_id="75" event_timestamp="2016-08-03 14:30:00">
            <td class="left">Aug 03, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">1.413M</span></td>
                <td class="noWrap">-1.363M</td>
                <td class="blackFont noWrap">1.671M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_332472" event_attr_id="75" event_timestamp="2016-07-27 14:30:00">
            <td class="left">Jul 27, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">1.671M</span></td>
                <td class="noWrap">-2.257M</td>
                <td class="blackFont noWrap">-2.342M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_332078" event_attr_id="75" event_timestamp="2016-07-20 14:30:00">
            <td class="left">Jul 20, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">-2.342M</span></td>
                <td class="noWrap">-2.100M</td>
                <td class="blackFont noWrap">-2.546M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_331819" event_attr_id="75" event_timestamp="2016-07-13 14:30:00">
            <td class="left">Jul 13, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">-2.546M</span></td>
                <td class="noWrap">-2.950M</td>
                <td class="blackFont noWrap">-2.223M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr><tr id="historicEvent_331341" event_attr_id="75" event_timestamp="2016-07-07 15:00:00">
            <td class="left">Jul 07, 2016 </td>
            <td class="left">11:00</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">-2.223M</span></td>
                <td class="noWrap">-2.250M</td>
                <td class="blackFont noWrap">-4.053M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_331085" event_attr_id="75" event_timestamp="2016-06-29 14:30:00">
            <td class="left">Jun 29, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">-4.053M</span></td>
                <td class="noWrap">-2.365M</td>
                <td class="blackFont noWrap">-0.917M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_330682" event_attr_id="75" event_timestamp="2016-06-22 14:30:00">
            <td class="left">Jun 22, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">-0.917M</span></td>
                <td class="noWrap">-1.671M</td>
                <td class="blackFont noWrap">-0.933M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_330361" event_attr_id="75" event_timestamp="2016-06-15 14:30:00">
            <td class="left">Jun 15, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">-0.933M</span></td>
                <td class="noWrap">-2.260M</td>
                <td class="blackFont noWrap">-3.226M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_330012" event_attr_id="75" event_timestamp="2016-06-08 14:30:00">
            <td class="left">Jun 08, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">-3.226M</span></td>
                <td class="noWrap">-2.740M</td>
                <td class="blackFont noWrap">-1.366M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_329615" event_attr_id="75" event_timestamp="2016-06-02 15:00:00">
            <td class="left">Jun 02, 2016 </td>
            <td class="left">11:00</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">-1.366M</span></td>
                <td class="noWrap">-2.490M</td>
                <td class="blackFont noWrap">-4.226M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr><tr id="historicEvent_329268" event_attr_id="75" event_timestamp="2016-05-25 14:30:00">
            <td class="left">May 25, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">-4.226M</span></td>
                <td class="noWrap">-2.450M</td>
                <td class="blackFont noWrap">1.310M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_328859" event_attr_id="75" event_timestamp="2016-05-18 14:30:00">
            <td class="left">May 18, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">1.310M</span></td>
                <td class="noWrap">-2.833M</td>
                <td class="blackFont noWrap">-3.410M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_328424" event_attr_id="75" event_timestamp="2016-05-11 14:30:00">
            <td class="left">May 11, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">-3.410M</span></td>
                <td class="noWrap">0.714M</td>
                <td class="blackFont noWrap">2.784M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_327809" event_attr_id="75" event_timestamp="2016-05-04 14:30:00">
            <td class="left">May 04, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">2.784M</span></td>
                <td class="noWrap">1.695M</td>
                <td class="blackFont noWrap">1.999M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_327450" event_attr_id="75" event_timestamp="2016-04-27 14:30:00">
            <td class="left">Apr 27, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">1.999M</span></td>
                <td class="noWrap">2.366M</td>
                <td class="blackFont noWrap">2.080M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_327052" event_attr_id="75" event_timestamp="2016-04-20 14:30:00">
            <td class="left">Apr 20, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">2.080M</span></td>
                <td class="noWrap">2.400M</td>
                <td class="blackFont noWrap">6.634M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr><tr id="historicEvent_326560" event_attr_id="75" event_timestamp="2016-04-13 14:30:00">
            <td class="left">Apr 13, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">6.634M</span></td>
                <td class="noWrap">1.850M</td>
                <td class="blackFont noWrap">-4.937M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_326217" event_attr_id="75" event_timestamp="2016-04-06 14:30:00">
            <td class="left">Apr 06, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">-4.937M</span></td>
                <td class="noWrap">3.150M</td>
                <td class="blackFont noWrap">2.299M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_325867" event_attr_id="75" event_timestamp="2016-03-30 14:30:00">
            <td class="left">Mar 30, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">2.299M</span></td>
                <td class="noWrap">3.300M</td>
                <td class="blackFont noWrap">9.357M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_325475" event_attr_id="75" event_timestamp="2016-03-23 14:30:00">
            <td class="left">Mar 23, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">9.357M</span></td>
                <td class="noWrap">3.090M</td>
                <td class="blackFont noWrap">1.317M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_325156" event_attr_id="75" event_timestamp="2016-03-16 14:30:00">
            <td class="left">Mar 16, 2016 </td>
            <td class="left">10:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">1.317M</span></td>
                <td class="noWrap">3.414M</td>
                <td class="blackFont noWrap">3.880M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_324809" event_attr_id="75" event_timestamp="2016-03-09 15:30:00">
            <td class="left">Mar 09, 2016 </td>
            <td class="left">11:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">3.880M</span></td>
                <td class="noWrap">3.867M</td>
                <td class="blackFont noWrap">10.374M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr><tr id="historicEvent_324422" event_attr_id="75" event_timestamp="2016-03-02 15:30:00">
            <td class="left">Mar 02, 2016 </td>
            <td class="left">11:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">10.374M</span></td>
                <td class="noWrap">3.604M</td>
                <td class="blackFont noWrap">3.502M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_324150" event_attr_id="75" event_timestamp="2016-02-24 15:30:00">
            <td class="left">Feb 24, 2016 </td>
            <td class="left">11:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">3.502M</span></td>
                <td class="noWrap">3.427M</td>
                <td class="blackFont noWrap">2.147M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_323673" event_attr_id="75" event_timestamp="2016-02-18 16:00:00">
            <td class="left">Feb 18, 2016 </td>
            <td class="left">12:00</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">2.147M</span></td>
                <td class="noWrap">3.920M</td>
                <td class="blackFont noWrap">-0.754M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_323287" event_attr_id="75" event_timestamp="2016-02-10 15:30:00">
            <td class="left">Feb 10, 2016 </td>
            <td class="left">11:30</td>
                            <td class="noWrap"><span class="greenFont" title="Better Than Expected">-0.754M</span></td>
                <td class="noWrap">3.550M</td>
                <td class="blackFont noWrap">7.792M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_322898" event_attr_id="75" event_timestamp="2016-02-03 15:30:00">
            <td class="left">Feb 03, 2016 </td>
            <td class="left">11:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">7.792M</span></td>
                <td class="noWrap">4.760M</td>
                <td class="blackFont noWrap">8.383M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr>
                <tr id="historicEvent_322602" event_attr_id="75" event_timestamp="2016-01-27 15:30:00">
            <td class="left">Jan 27, 2016 </td>
            <td class="left">11:30</td>
                            <td class="noWrap"><span class="redFont" title="Worse Than Expected">8.383M</span></td>
                <td class="noWrap">3.277M</td>
                <td class="blackFont noWrap">3.979M</td>
                <td class="icon center"><i class="diamondNewEmptyIcon"></i></td>
                    </tr></tbody>
                    """

if __name__ == '__main__':
    root = ET.fromstring(html)

    print 'date|time|color|actual|forcast|prev'
    for data in root.iterfind("./tr"):
        dt = data[0].text
        tm = data[1].text
        color = data[2][0].attrib['class']
        actual = data[2][0].text
        forcast = data[3].text
        prev = data[4].text
        print '{}|{}|{}|{}|{}|{}'.format(dt, tm, color, actual, forcast, prev)
        assert color in ['greenFont', 'redFont']
        actual_more_than_forcast = float(actual.strip('M')) > float(forcast.strip('M'))
        assert (actual_more_than_forcast and color == 'redFont') or ((not actual_more_than_forcast) and color == 'greenFont')



